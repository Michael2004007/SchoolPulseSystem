from flask import Blueprint, render_template
from flask_login import login_required
from DAO.pulserasDAO import PulseraDAO
import os

inicio_bp = Blueprint('inicio', __name__)


@inicio_bp.route('/')
@login_required
def index():
    pulseras = PulseraDAO.seleccionar()
    total_pulseras = len(pulseras) if pulseras else 0
    total_repartidas = len([p for p in pulseras if p.estado == 'repartida']) if pulseras else 0
    total_pagadas = len([p for p in pulseras if p.estado == 'pagada']) if pulseras else 0

    logo_existe = False
    logo_ext = 'png'
    upload_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
    for ext in ['png', 'jpg', 'jpeg', 'webp']:
        if os.path.exists(os.path.join(upload_path, f'logo_colegio.{ext}')):
            logo_existe = True
            logo_ext = ext
            break

    return render_template('inicio/index.html',
                           total_pulseras=total_pulseras,
                           total_repartidas=total_repartidas,
                           total_pagadas=total_pagadas,
                           logo_existe=logo_existe,
                           logo_ext=logo_ext)