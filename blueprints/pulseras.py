from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from DAO.pulserasDAO import PulseraDAO
from entidades.Pulsera import Pulsera

pulseras_bp = Blueprint('pulseras', __name__, url_prefix='/pulseras')


@pulseras_bp.route('/')
@login_required
def index():
    pulseras = PulseraDAO.seleccionar()
    total = len(pulseras) if pulseras else 0
    disponibles = len([p for p in pulseras if p.estado == 'disponible']) if pulseras else 0
    repartidas = len([p for p in pulseras if p.estado == 'repartida']) if pulseras else 0
    pagadas = len([p for p in pulseras if p.estado == 'pagada']) if pulseras else 0
    return render_template('pulseras/index.html',
                           pulseras=pulseras,
                           total=total,
                           disponibles=disponibles,
                           repartidas=repartidas,
                           pagadas=pagadas)


@pulseras_bp.route('/cargar', methods=['GET', 'POST'])
@login_required
def cargar():
    if request.method == 'POST':
        desde = int(request.form['desde'])
        hasta = int(request.form['hasta'])

        creadas = 0
        duplicadas = []

        for numero in range(desde, hasta + 1):
            pulsera = Pulsera(id=numero)
            resultado = PulseraDAO.insertar(pulsera)
            if resultado:
                creadas += 1
            else:
                duplicadas.append(numero)

        maximo_actual = PulseraDAO.obtener_maximo_id()
        siguiente = maximo_actual + 1

        if creadas == 0 and duplicadas:
            flash(f'🚫 Ninguna pulsera fue creada. El rango del {desde} al {hasta} ya existe en el sistema. ¿Querés agregar más? Podés crear a partir del #{siguiente}.', 'warning')
        elif creadas > 0 and duplicadas:
            flash(f'⚠️ Se crearon {creadas} pulseras nuevas. Algunas ya existían. Podés seguir agregando desde el #{siguiente}.', 'warning')
        else:
            flash(f'✅ ¡Listo! Se crearon {creadas} pulseras correctamente, del #{desde} al #{hasta}.', 'success')

        return redirect(url_for('pulseras.index'))
    return render_template('pulseras/cargar.html')