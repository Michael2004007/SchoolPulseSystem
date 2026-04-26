from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from DAO.pulserasDAO import PulseraDAO
from DAO.cobroDAO import CobroDAO
from DAO.repartoDAO import RepartoDAO
from DAO.alumnoDAO import AlumnoDAO
from entidades.Cobro import Cobro
from entidades.Pulsera import Pulsera

porton_bp = Blueprint('porton', __name__, url_prefix='/porton')

MONTO_PULSERA = 20000


@porton_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    resultado = None
    numero = request.args.get('numero', '').strip()

    if numero:
        try:
            numero_int = int(numero)
            pulsera = PulseraDAO.seleccionar_por_id(Pulsera(id=numero_int))
            if pulsera:
                resultado = {'pulsera': pulsera, 'alumno': None, 'cobro': None}
                repartos = RepartoDAO.seleccionar_por_pulsera(numero_int)
                if repartos:
                    alumno = AlumnoDAO.seleccionar_por_id(repartos.alumno_id)
                    resultado['alumno'] = alumno
                cobro = CobroDAO.seleccionar_por_pulsera(numero_int)
                resultado['cobro'] = cobro
            else:
                flash(f'⚠️ La pulsera #{numero} no existe en el sistema.', 'warning')
        except ValueError:
            flash('⚠️ Ingresá un número de pulsera válido.', 'warning')

    return render_template('porton/index.html', resultado=resultado, numero=numero)


@porton_bp.route('/pagar/<int:pulsera_id>', methods=['POST'])
@login_required
def pagar(pulsera_id):
    cobro = Cobro(pulsera_id=pulsera_id, monto=MONTO_PULSERA)
    CobroDAO.insertar(cobro)
    PulseraDAO.actualizar(Pulsera(id=pulsera_id, estado='pagada'))
    flash(f'✅ Pulsera #{pulsera_id} cobrada correctamente.', 'success')
    return redirect(url_for('porton.index', numero=pulsera_id))