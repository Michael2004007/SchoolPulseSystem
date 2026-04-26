from flask import Blueprint, render_template
from flask_login import login_required
from DAO.pulserasDAO import PulseraDAO
from conexion import Conexion

inicio_bp = Blueprint('inicio', __name__)


@inicio_bp.route('/')
@login_required
def index():
    pulseras = PulseraDAO.seleccionar()
    total_pulseras = len(pulseras) if pulseras else 0
    total_repartidas = len([p for p in pulseras if p.estado == 'repartida']) if pulseras else 0
    total_pagadas = len([p for p in pulseras if p.estado == 'pagada']) if pulseras else 0

    logo_existe = False
    conexion = None
    try:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute('SELECT logo FROM usuario WHERE logo IS NOT NULL LIMIT 1')
        row = cursor.fetchone()
        logo_existe = row is not None and row[0] is not None
    except:
        logo_existe = False
    finally:
        if conexion:
            cursor.close()
            Conexion.liberar_conexion(conexion)

    return render_template('inicio/index.html',
                           total_pulseras=total_pulseras,
                           total_repartidas=total_repartidas,
                           total_pagadas=total_pagadas,
                           logo_existe=logo_existe,
                           logo_ext='')