from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from DAO.repartoDAO import RepartoDAO
from DAO.alumnoDAO import AlumnoDAO
from DAO.pulserasDAO import PulseraDAO
from entidades.Reparto import Reparto
from entidades.Alumno import Alumno
from entidades.Pulsera import Pulsera
import re
import openpyxl
import io

reparto_bp = Blueprint('reparto', __name__, url_prefix='/reparto')


def normalizar_curso(curso):
    curso = curso.upper().strip()
    curso = re.sub(r'\s+', ' ', curso)
    curso = re.sub(r'([0-9]+)\s*([A-Z]+)', r'\1 \2', curso)
    return curso


@reparto_bp.route('/')
@login_required
def index():
    repartos = RepartoDAO.seleccionar_agrupado()
    total_alumnos = len(repartos) if repartos else 0
    total_pulseras = sum(len(r.pulseras) for r in repartos) if repartos else 0
    pulseras_todas = PulseraDAO.seleccionar()
    disponibles = len([p for p in pulseras_todas if p.estado == 'disponible']) if pulseras_todas else 0
    return render_template('reparto/index.html',
                           repartos=repartos,
                           total_alumnos=total_alumnos,
                           total_pulseras=total_pulseras,
                           disponibles=disponibles)


@reparto_bp.route('/asignar', methods=['GET', 'POST'])
@login_required
def asignar():
    pulseras_todas = PulseraDAO.seleccionar()
    disponibles = len([p for p in pulseras_todas if p.estado == 'disponible']) if pulseras_todas else 0
    proxima = PulseraDAO.obtener_proxima_disponible()

    if request.method == 'POST':
        nombre = request.form['nombre'].strip().title()
        apellido = request.form['apellido'].strip().title()
        curso = normalizar_curso(request.form['curso'])
        pulsera_desde = int(request.form['pulsera_desde'])
        pulsera_hasta = int(request.form['pulsera_hasta'])

        disponibles_en_rango = []
        no_disponibles_en_rango = []

        for numero in range(pulsera_desde, pulsera_hasta + 1):
            pulsera = PulseraDAO.seleccionar_por_id(Pulsera(id=numero))
            if pulsera and pulsera.estado == 'disponible':
                disponibles_en_rango.append(numero)
            else:
                no_disponibles_en_rango.append(numero)

        if len(disponibles_en_rango) == 0:
            form_data = {
                'nombre': nombre,
                'apellido': apellido,
                'curso': curso,
                'pulsera_desde': pulsera_desde,
                'pulsera_hasta': pulsera_hasta
            }
            return render_template('reparto/asignar.html',
                                   disponibles=disponibles,
                                   proxima=proxima,
                                   error_rango=True,
                                   form_data=form_data)

        alumno = Alumno(nombre=nombre, apellido=apellido, curso=curso)
        alumno_id = AlumnoDAO.insertar(alumno)

        for numero in disponibles_en_rango:
            reparto = Reparto(alumno_id=alumno_id, pulsera_id=numero)
            RepartoDAO.insertar(reparto)
            PulseraDAO.actualizar(Pulsera(id=numero, estado='repartida'))

        if no_disponibles_en_rango:
            flash(f'⚠️ Se asignaron {len(disponibles_en_rango)} pulseras a {nombre} {apellido}. Las #{", #".join(map(str, no_disponibles_en_rango))} ya estaban ocupadas.', 'warning')
        else:
            flash(f'✅ ¡Listo! Se asignaron {len(disponibles_en_rango)} pulseras a {nombre} {apellido} del curso {curso}.', 'success')

        return redirect(url_for('reparto.index'))

    return render_template('reparto/asignar.html',
                           disponibles=disponibles,
                           proxima=proxima,
                           error_rango=False,
                           form_data=None)


@reparto_bp.route('/asignar_existente/<int:alumno_id>', methods=['GET', 'POST'])
@login_required
def asignar_existente(alumno_id):
    alumno = AlumnoDAO.seleccionar_por_id(alumno_id)
    if not alumno:
        flash('❌ Alumno no encontrado.', 'danger')
        return redirect(url_for('reparto.index'))

    pulseras_todas = PulseraDAO.seleccionar()
    disponibles = len([p for p in pulseras_todas if p.estado == 'disponible']) if pulseras_todas else 0
    proxima = PulseraDAO.obtener_proxima_disponible()

    if request.method == 'POST':
        pulsera_desde = int(request.form['pulsera_desde'])
        pulsera_hasta = int(request.form['pulsera_hasta'])

        disponibles_en_rango = []
        no_disponibles_en_rango = []

        for numero in range(pulsera_desde, pulsera_hasta + 1):
            pulsera = PulseraDAO.seleccionar_por_id(Pulsera(id=numero))
            if pulsera and pulsera.estado == 'disponible':
                disponibles_en_rango.append(numero)
            else:
                no_disponibles_en_rango.append(numero)

        if len(disponibles_en_rango) == 0:
            flash('❌ No hay pulseras disponibles en ese rango.', 'danger')
            return render_template('reparto/asignar_existente.html',
                                   alumno=alumno,
                                   disponibles=disponibles,
                                   proxima=proxima)

        for numero in disponibles_en_rango:
            reparto = Reparto(alumno_id=alumno_id, pulsera_id=numero)
            RepartoDAO.insertar(reparto)
            PulseraDAO.actualizar(Pulsera(id=numero, estado='repartida'))

        if no_disponibles_en_rango:
            flash(f'⚠️ Se asignaron {len(disponibles_en_rango)} pulseras. Las #{", #".join(map(str, no_disponibles_en_rango))} ya estaban ocupadas.', 'warning')
        else:
            flash(f'✅ Se asignaron {len(disponibles_en_rango)} pulseras a {alumno.nombre} {alumno.apellido}.', 'success')

        return redirect(url_for('reparto.index'))

    return render_template('reparto/asignar_existente.html',
                           alumno=alumno,
                           disponibles=disponibles,
                           proxima=proxima)


@reparto_bp.route('/cargar_excel', methods=['GET', 'POST'])
@login_required
def cargar_excel():
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('❌ No se seleccionó ningún archivo.', 'danger')
            return redirect(url_for('reparto.cargar_excel'))

        archivo = request.files['archivo']
        if archivo.filename == '' or not archivo.filename.endswith('.xlsx'):
            flash('❌ El archivo debe ser un Excel (.xlsx).', 'danger')
            return redirect(url_for('reparto.cargar_excel'))

        try:
            contenido = archivo.read()
            wb = openpyxl.load_workbook(io.BytesIO(contenido))
            ws = wb.active

            insertados = 0
            errores = 0

            for fila in ws.iter_rows(min_row=2, values_only=True):
                if not fila or not fila[0]:
                    continue
                try:
                    nombre = str(fila[0]).strip().title()
                    apellido = str(fila[1]).strip().title()
                    curso = normalizar_curso(str(fila[2]))
                    alumno = Alumno(nombre=nombre, apellido=apellido, curso=curso)
                    AlumnoDAO.insertar(alumno)
                    insertados += 1
                except Exception:
                    errores += 1

            if errores:
                flash(f'✅ Se cargaron {insertados} alumnos. ⚠️ {errores} filas con error fueron ignoradas.', 'warning')
            else:
                flash(f'✅ Se cargaron {insertados} alumnos correctamente.', 'success')

        except Exception as e:
            flash(f'❌ Error al procesar el archivo: {e}', 'danger')

        return redirect(url_for('reparto.cargar_excel'))

    alumnos = AlumnoDAO.seleccionar()
    return render_template('reparto/cargar_excel.html', alumnos=alumnos)


@reparto_bp.route('/eliminar/<int:alumno_id>', methods=['POST'])
@login_required
def eliminar(alumno_id):
    pulseras = RepartoDAO.eliminar_asignacion(alumno_id)
    if pulseras is not None:
        for pulsera_id in pulseras:
            PulseraDAO.actualizar(Pulsera(id=pulsera_id, estado='disponible'))
        flash(f'✅ Asignación eliminada. Las pulseras #{", #".join(map(str, pulseras))} volvieron a estar disponibles.', 'success')
    else:
        flash('❌ Ocurrió un error al eliminar la asignación.', 'danger')
    return redirect(url_for('reparto.index'))