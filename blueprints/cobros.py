from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from DAO.cobroDAO import CobroDAO
from DAO.pulserasDAO import PulseraDAO
from DAO.alumnoDAO import AlumnoDAO
from entidades.Cobro import Cobro
from entidades.Pulsera import Pulsera

cobro_bp = Blueprint('cobro', __name__, url_prefix='/cobro')

MONTO_PULSERA = 20000


def normalizar_curso(curso):
    return ' '.join(curso.upper().split())


@cobro_bp.route('/')
@login_required
def index():
    busqueda = request.args.get('busqueda', '').strip()
    curso = request.args.get('curso', '').strip()

    if busqueda:
        alumnos = AlumnoDAO.buscar_por_nombre(busqueda)
    elif curso:
        alumnos = AlumnoDAO.buscar_por_curso(normalizar_curso(curso))
    else:
        alumnos = AlumnoDAO.seleccionar()

    if alumnos:
        for a in alumnos:
            pulseras = CobroDAO.seleccionar_pulseras_por_alumno(a.id)
            a.total_pulseras = len(pulseras) if pulseras else 0
            pagadas = [p for p in pulseras if p.estado == 'pagada'] if pulseras else []
            a.todas_pagadas = len(pagadas) == a.total_pulseras and a.total_pulseras > 0
            a.algunas_pagadas = 0 < len(pagadas) < a.total_pulseras

    total = len(alumnos) if alumnos else 0
    pendientes = len([a for a in alumnos if not a.todas_pagadas]) if alumnos else 0
    pagados = len([a for a in alumnos if a.todas_pagadas]) if alumnos else 0

    return render_template('cobro/index.html',
                           alumnos=alumnos,
                           busqueda=busqueda,
                           curso=curso,
                           total=total,
                           pendientes=pendientes,
                           pagados=pagados)


@cobro_bp.route('/detalle/<int:alumno_id>')
@login_required
def detalle(alumno_id):
    alumno = AlumnoDAO.seleccionar_por_id(alumno_id)
    pulseras = CobroDAO.seleccionar_pulseras_por_alumno(alumno_id)
    total_pulseras = len(pulseras) if pulseras else 0
    pagadas = len([p for p in pulseras if p.estado == 'pagada']) if pulseras else 0
    pendientes = total_pulseras - pagadas
    return render_template('cobro/detalle.html',
                           alumno=alumno,
                           pulseras=pulseras,
                           total_pulseras=total_pulseras,
                           pagadas=pagadas,
                           pendientes=pendientes,
                           monto_pulsera=MONTO_PULSERA)


@cobro_bp.route('/pagar/<int:pulsera_id>', methods=['POST'])
@login_required
def pagar(pulsera_id):
    alumno_id = request.form['alumno_id']
    monto = request.form['monto']
    cobro = Cobro(pulsera_id=pulsera_id, monto=monto)
    CobroDAO.insertar(cobro)
    PulseraDAO.actualizar(Pulsera(id=pulsera_id, estado='pagada'))
    flash(f'✅ Pulsera #{pulsera_id} marcada como pagada.', 'success')
    return redirect(url_for('cobro.detalle', alumno_id=alumno_id))


@cobro_bp.route('/desmarcar/<int:pulsera_id>', methods=['POST'])
@login_required
def desmarcar(pulsera_id):
    alumno_id = request.form['alumno_id']
    CobroDAO.eliminar_cobro(pulsera_id)
    PulseraDAO.actualizar(Pulsera(id=pulsera_id, estado='repartida'))
    flash(f'↩️ Pulsera #{pulsera_id} desmarcada correctamente.', 'warning')
    return redirect(url_for('cobro.detalle', alumno_id=alumno_id))