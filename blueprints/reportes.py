from flask import Blueprint, render_template, make_response
from flask_login import login_required
from DAO.reportesDAO import ReporteDAO
from DAO.pulserasDAO import PulseraDAO
from io import BytesIO

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

MONTO_PULSERA = 20000


def normalizar_curso(curso):
    return ' '.join(curso.upper().split())


@reportes_bp.route('/')
@login_required
def index():
    pulseras = PulseraDAO.seleccionar()
    total = len(pulseras) if pulseras else 0
    disponibles = len([p for p in pulseras if p.estado == 'disponible']) if pulseras else 0
    repartidas = len([p for p in pulseras if p.estado == 'repartida']) if pulseras else 0
    pagadas = len([p for p in pulseras if p.estado == 'pagada']) if pulseras else 0
    total_recaudado = pagadas * MONTO_PULSERA
    ya_cobrado = pagadas * MONTO_PULSERA
    por_cobrar = repartidas * MONTO_PULSERA
    potencial_asignadas = (repartidas + pagadas) * MONTO_PULSERA
    potencial_total = total * MONTO_PULSERA
    return render_template('reportes/index.html',
                           total=total,
                           disponibles=disponibles,
                           repartidas=repartidas,
                           pagadas=pagadas,
                           total_recaudado=total_recaudado,
                           ya_cobrado=ya_cobrado,
                           por_cobrar=por_cobrar,
                           potencial_asignadas=potencial_asignadas,
                           potencial_total=potencial_total)


@reportes_bp.route('/pulseras')
@login_required
def pulseras():
    reporte = ReporteDAO.reporte_pulseras()
    return render_template('reportes/pulseras.html', reporte=reporte)


@reportes_bp.route('/deudores')
@login_required
def deudores():
    deudores = ReporteDAO.reporte_deudores()
    return render_template('reportes/deudores.html', deudores=deudores)


@reportes_bp.route('/pagados')
@login_required
def pagados():
    pagados = ReporteDAO.reporte_pagados()
    return render_template('reportes/pagados.html', pagados=pagados)


@reportes_bp.route('/cursos')
@login_required
def cursos():
    cursos = ReporteDAO.reporte_cursos()
    return render_template('reportes/cursos.html', cursos=cursos)


@reportes_bp.route('/cursos/<path:curso>')
@login_required
def detalle_curso(curso):
    curso = normalizar_curso(curso)
    alumnos = ReporteDAO.reporte_por_curso(curso)
    total = len(alumnos)
    pagados = sum(1 for a in alumnos if a[5] == a[6])
    pendientes = total - pagados
    return render_template('reportes/detalle_curso.html',
                           curso=curso,
                           alumnos=alumnos,
                           total=total,
                           pagados=pagados,
                           pendientes=pendientes)


@reportes_bp.route('/pdf/general')
@login_required
def pdf_general():
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import HRFlowable

    pulseras = PulseraDAO.seleccionar()
    total = len(pulseras) if pulseras else 0
    disponibles = len([p for p in pulseras if p.estado == 'disponible']) if pulseras else 0
    repartidas = len([p for p in pulseras if p.estado == 'repartida']) if pulseras else 0
    pagadas = len([p for p in pulseras if p.estado == 'pagada']) if pulseras else 0

    ya_cobrado = pagadas * MONTO_PULSERA
    por_cobrar = repartidas * MONTO_PULSERA
    potencial_asignadas = (repartidas + pagadas) * MONTO_PULSERA
    potencial_total = total * MONTO_PULSERA
    porcentaje = int((pagadas / (repartidas + pagadas)) * 100) if (repartidas + pagadas) > 0 else 0

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=1.5*cm, leftMargin=1.5*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    elementos = []

    s_titulo = ParagraphStyle('titulo', fontName='Helvetica-Bold', fontSize=22,
                              textColor=colors.HexColor('#4F46E5'), leading=28)
    s_sub = ParagraphStyle('sub', fontName='Helvetica', fontSize=9,
                           textColor=colors.HexColor('#9CA3AF'), leading=14)
    s_seccion = ParagraphStyle('seccion', fontName='Helvetica-Bold', fontSize=11,
                               textColor=colors.HexColor('#0F1117'), leading=16)
    s_nota = ParagraphStyle('nota', fontName='Helvetica', fontSize=8,
                            textColor=colors.HexColor('#9CA3AF'), leading=12)

    def tarjeta_valor(label, valor, bg, color_texto, borde):
        s_val = ParagraphStyle('val', fontName='Helvetica-Bold', fontSize=13,
                               textColor=colors.HexColor(color_texto), leading=18)
        s_lab = ParagraphStyle('lab', fontName='Helvetica', fontSize=8,
                               textColor=colors.HexColor('#6B7280'), leading=12)
        t = Table(
            [[Paragraph(valor, s_val)],
             [Paragraph(label, s_lab)]],
            colWidths=[4.3*cm],
            rowHeights=[1*cm, 0.65*cm],
            style=TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg)),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor(borde)),
                ('LEFTPADDING', (0,0), (-1,-1), 10),
                ('RIGHTPADDING', (0,0), (-1,-1), 10),
                ('TOPPADDING', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ])
        )
        return t

    def fila_tarjetas(tarjetas):
        return Table(
            [tarjetas],
            colWidths=[4.3*cm, 4.3*cm, 4.3*cm, 4.3*cm],
            style=TableStyle([
                ('LEFTPADDING', (0,0), (-1,-1), 3),
                ('RIGHTPADDING', (0,0), (-1,-1), 3),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ])
        )

    elementos.append(Paragraph('Reporte General', s_titulo))
    elementos.append(Spacer(1, 0.2*cm))
    elementos.append(Paragraph('Colegio Nacional Panchito López — SchoolPulse 2026', s_sub))
    elementos.append(Spacer(1, 0.6*cm))

    elementos.append(Paragraph('Estado de pulseras', s_seccion))
    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(fila_tarjetas([
        tarjeta_valor('Total pulseras', str(total), '#EEF2FF', '#4F46E5', '#C7D2FE'),
        tarjeta_valor('Pendientes cobro', str(repartidas), '#FFFBEB', '#D97706', '#FDE68A'),
        tarjeta_valor('Pagadas', str(pagadas), '#ECFDF5', '#059669', '#A7F3D0'),
        tarjeta_valor('Gs. recaudados', f'Gs. {ya_cobrado:,.0f}', '#EEF2FF', '#4F46E5', '#C7D2FE'),
    ]))
    elementos.append(Spacer(1, 0.7*cm))

    elementos.append(Paragraph('Previsiones de recaudación', s_seccion))
    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(fila_tarjetas([
        tarjeta_valor('Ya cobrado', f'Gs. {ya_cobrado:,.0f}', '#ECFDF5', '#059669', '#A7F3D0'),
        tarjeta_valor('Falta cobrar', f'Gs. {por_cobrar:,.0f}', '#FFFBEB', '#D97706', '#FDE68A'),
        tarjeta_valor('Potencial asignadas', f'Gs. {potencial_asignadas:,.0f}', '#EEF2FF', '#4F46E5', '#C7D2FE'),
        tarjeta_valor('Potencial máximo', f'Gs. {potencial_total:,.0f}', '#F9FAFB', '#6B7280', '#E5E7EB'),
    ]))
    elementos.append(Spacer(1, 0.7*cm))

    elementos.append(Paragraph('Progreso de cobro', s_seccion))
    elementos.append(Spacer(1, 0.3*cm))

    ancho_total = 17.5*cm
    ancho_fill = max(ancho_total * porcentaje / 100, 0.1*cm)
    ancho_resto = ancho_total - ancho_fill

    if ancho_resto > 0.1*cm:
        barra = Table([['', '']], colWidths=[ancho_fill, ancho_resto], rowHeights=[0.35*cm])
        barra.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#4F46E5')),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor('#E8EAF0')),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
    else:
        barra = Table([['']], colWidths=[ancho_total], rowHeights=[0.35*cm])
        barra.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#4F46E5')),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))

    elementos.append(barra)
    elementos.append(Spacer(1, 0.3*cm))

    s_prog_gris = ParagraphStyle('pg', fontName='Helvetica', fontSize=8,
                                 textColor=colors.HexColor('#9CA3AF'), leading=12)
    s_prog_warn = ParagraphStyle('pw', fontName='Helvetica', fontSize=8,
                                 textColor=colors.HexColor('#D97706'), leading=12)
    s_prog_ok = ParagraphStyle('po', fontName='Helvetica', fontSize=8,
                               textColor=colors.HexColor('#059669'), leading=12)

    fila_prog = Table([[
        Paragraph(f'Disponibles: {disponibles}', s_prog_gris),
        Paragraph(f'Pendientes: {repartidas}', s_prog_warn),
        Paragraph(f'Cobradas: {pagadas} ({porcentaje}%)', s_prog_ok),
    ]],
    colWidths=[5.8*cm, 5.8*cm, 5.9*cm],
    style=TableStyle([
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('ALIGN', (2,0), (2,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elementos.append(fila_prog)
    elementos.append(Spacer(1, 0.6*cm))
    elementos.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#E8EAF0')))
    elementos.append(Spacer(1, 0.3*cm))
    elementos.append(Paragraph(f'Monto unitario por pulsera: Gs. {MONTO_PULSERA:,.0f}', s_nota))

    doc.build(elementos)
    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_general.pdf'
    return response


@reportes_bp.route('/cursos/pdf/<path:curso>')
@login_required
def pdf_curso(curso):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm

    curso = normalizar_curso(curso)
    alumnos = ReporteDAO.reporte_por_curso(curso)
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    s_titulo = ParagraphStyle('titulo', fontName='Helvetica-Bold', fontSize=18,
                              textColor=colors.HexColor('#4F46E5'), leading=24)
    s_sub = ParagraphStyle('sub', fontName='Helvetica', fontSize=9,
                           textColor=colors.HexColor('#9CA3AF'), leading=14)
    s_resumen = ParagraphStyle('resumen', fontName='Helvetica', fontSize=9,
                               textColor=colors.HexColor('#6B7280'), leading=12)

    elementos = []
    elementos.append(Paragraph(f'Reporte del Curso: {curso}', s_titulo))
    elementos.append(Spacer(1, 0.2*cm))
    elementos.append(Paragraph('Colegio Nacional Panchito López — SchoolPulse 2026', s_sub))
    elementos.append(Spacer(1, 0.5*cm))

    datos = [['#', 'Nombre', 'Apellido', 'Pulseras', 'Pagadas', 'Estado']]
    for i, a in enumerate(alumnos, 1):
        estado = 'Pagado' if a[5] == a[6] else 'Pendiente'
        datos.append([str(i), a[1], a[2], str(a[4]), f"{a[5]}/{a[6]}", estado])

    tabla = Table(datos, colWidths=[1*cm, 4*cm, 4*cm, 4*cm, 2.5*cm, 2.5*cm])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6FB')]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E8EAF0')),
        ('ROWHEIGHT', (0, 0), (-1, -1), 22),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 0.5*cm))

    pagados_count = sum(1 for a in alumnos if a[5] == a[6])
    elementos.append(Paragraph(
        f'Total alumnos: {len(alumnos)}  |  Pagados: {pagados_count}  |  Pendientes: {len(alumnos) - pagados_count}',
        s_resumen))

    doc.build(elementos)
    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=curso_{curso.replace(" ", "_")}.pdf'
    return response