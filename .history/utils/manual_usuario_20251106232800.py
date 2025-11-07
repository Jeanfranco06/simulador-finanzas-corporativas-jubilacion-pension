from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

def crear_caja_info(icon, title, content, color=None):
    """Helper para crear cajas de información con diseño consistente"""
    if color is None:
        color = colors.HexColor('#0ea5e9')
    
    data = [[
        Paragraph(f'<font size="20">{icon}</font>', ParagraphStyle('icon', alignment=TA_CENTER)),
        Paragraph(f'<b>{title}</b><br/><font size="10">{content}</font>', 
                 ParagraphStyle('content', fontSize=10, leading=14))
    ]]
    
    table = Table(data, colWidths=[2*cm, 14*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), color),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#f1f5f9')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, color),
    ]))
    return table

def crear_manual_usuario():
    """Crear manual de usuario con diseño profesional y atractivo"""

    # Directorios
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'docs')
    images_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'images')
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    filename = os.path.join(output_dir, 'manual_usuario.pdf')

    # Configuración del documento
    doc = SimpleDocTemplate(
        filename, 
        pagesize=A4, 
        rightMargin=2*cm, 
        leftMargin=2*cm, 
        topMargin=2*cm, 
        bottomMargin=2*cm
    )

    # Colores corporativos
    COLOR_PRINCIPAL = colors.HexColor('#0ea5e9')
    COLOR_SECUNDARIO = colors.HexColor('#06b6d4')
    COLOR_ACENTO = colors.HexColor('#8b5cf6')
    COLOR_EXITO = colors.HexColor('#10b981')
    COLOR_TEXTO = colors.HexColor('#1e293b')
    COLOR_FONDO = colors.HexColor('#f1f5f9')

    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=36,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=COLOR_PRINCIPAL,
        fontName='Helvetica-Bold',
        leading=42
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=22,
        spaceAfter=25,
        alignment=TA_CENTER,
        textColor=COLOR_SECUNDARIO,
        fontName='Helvetica-Bold',
        leading=26
    )

    section_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=15,
        spaceBefore=20,
        textColor=COLOR_PRINCIPAL,
        fontName='Helvetica-Bold',
        backColor=COLOR_FONDO,
        borderPadding=10,
        leading=22
    )

    subsection_style = ParagraphStyle(
        'CustomSubsection',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=15,
        textColor=COLOR_ACENTO,
        fontName='Helvetica-Bold',
        leading=18
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        textColor=COLOR_TEXTO,
        leading=16
    )

    content = []

    # ==================== PORTADA ====================
    content.append(Spacer(1, 1*cm))
    
    # Logo universidad
    logo_path = os.path.join(images_dir, 'logo_universidad.png')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=4*cm, height=4*cm)
            logo.hAlign = 'CENTER'
            content.append(logo)
            content.append(Spacer(1, 0.5*cm))
        except:
            pass
    
    content.append(Paragraph("💰 TU RETIRO SEGURO", title_style))
    content.append(Spacer(1, 0.3*cm))
    content.append(Paragraph("Simulador Financiero Inteligente", subtitle_style))
    content.append(Spacer(1, 0.5*cm))
    
    subtitle_text = '<font size="14" color="#475569"><i>Tu Compañero en el Camino hacia la Libertad Financiera</i></font>'
    content.append(Paragraph(subtitle_text, ParagraphStyle('center', alignment=TA_CENTER)))
    content.append(Spacer(1, 1.5*cm))

    # Imagen dashboard principal
    dashboard_path = os.path.join(images_dir, 'dashboard_principal.png')
    if os.path.exists(dashboard_path):
        try:
            dashboard = Image(dashboard_path, width=14*cm, height=9*cm)
            dashboard.hAlign = 'CENTER'
            content.append(dashboard)
        except:
            placeholder_table = Table(
                [['📊 INTERFAZ INTUITIVA Y MODERNA']],
                colWidths=[14*cm],
                rowHeights=[9*cm]
            )
            placeholder_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), COLOR_FONDO),
                ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_PRINCIPAL),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 20),
                ('BOX', (0, 0), (-1, -1), 2, COLOR_PRINCIPAL),
            ]))
            content.append(placeholder_table)
    content.append(Spacer(1, 1*cm))

    # Info publicación
    pub_data = [
        ['Manual del Usuario', 'Versión 2.0 Profesional'],
        ['Simulador Financiero', 'Noviembre 2025'],
    ]
    
    pub_table = Table(pub_data, colWidths=[8*cm, 8*cm])
    pub_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_FONDO),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLOR_TEXTO),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_PRINCIPAL),
    ]))
    content.append(pub_table)
    content.append(Spacer(1, 0.8*cm))

    # Equipo
    team_title = Paragraph(
        '<b>Desarrollado por: Unidad II - Finanzas Corporativas</b>', 
        ParagraphStyle('team_title', alignment=TA_CENTER, fontSize=12, 
                      textColor=COLOR_PRINCIPAL, fontName='Helvetica-Bold')
    )
    content.append(team_title)
    content.append(Spacer(1, 0.4*cm))
    
    team_data = [
        ['<b>Integrantes del Equipo</b>'],
        ['Gonzales Esquivel, Jeanfranco Jefferson'],
        ['Moreno Aguilar, Dalessandro Zahit'],
        ['Rodríguez Sandoval, Harry Sly'],
        ['Velásquez García, Ricardo Bernardo'],
        ['Carril Freyre, Justin Ismael Neil'],
    ]
    
    team_table = Table(team_data, colWidths=[16*cm])
    team_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLOR_TEXTO),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_PRINCIPAL),
    ]))
    content.append(team_table)
    content.append(Spacer(1, 0.8*cm))

    # Cita inspiracional
    quote_data = [[Paragraph(
        '<i>"El futuro pertenece a quienes creen en la belleza de sus sueños"</i><br/><br/>'
        '— Eleanor Roosevelt',
        ParagraphStyle('quote', fontSize=13, alignment=TA_CENTER, textColor=COLOR_ACENTO, 
                      fontName='Helvetica-Oblique', leading=18)
    )]]
    
    quote_table = Table(quote_data, colWidths=[15*cm])
    quote_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_FONDO),
        ('BOX', (0, 0), (-1, -1), 2, COLOR_ACENTO),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    content.append(quote_table)

    content.append(PageBreak())

    # ==================== ÍNDICE ====================
    content.append(Paragraph("📋 ÍNDICE EJECUTIVO", section_style))
    content.append(Spacer(1, 0.5*cm))

    indice_data = [
        ['Cap.', 'Título', 'Pág.'],
        ['🎯 1', 'Introducción y Beneficios Clave', '3'],
        ['🚀 2', 'Primeros Pasos', '6'],
        ['👤 3', 'Sistema de Usuarios', '9'],
        ['💼 4', 'Módulo A: Crecimiento de Cartera', '12'],
        ['🏖️ 5', 'Módulo B: Proyección de Jubilación', '15'],
        ['📈 6', 'Módulo C: Valoración de Bonos', '18'],
        ['🎲 7', 'Análisis de Escenarios', '21'],
        ['📊 8', 'Gamificación', '24'],
        ['👥 9', 'Comparación Social', '27'],
        ['🛒 10', 'Marketplace', '30'],
        ['📄 11', 'Reportes PDF', '33'],
        ['🔧 12', 'Soporte', '36'],
        ['📚 13', 'Glosario', '39'],
    ]
    
    indice_table = Table(indice_data, colWidths=[2*cm, 12*cm, 2*cm])
    indice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLOR_TEXTO),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_PRINCIPAL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_FONDO, colors.white]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    content.append(indice_table)

    content.append(PageBreak())

    # ==================== CAPÍTULO 1: INTRODUCCIÓN ====================
    content.append(Paragraph("🎯 1. INTRODUCCIÓN Y BENEFICIOS CLAVE", section_style))
    content.append(Spacer(1, 0.5*cm))

    intro_img_path = os.path.join(images_dir, 'modulo_a_captura.png')
    if os.path.exists(intro_img_path):
        try:
            intro_img = Image(intro_img_path, width=15*cm, height=8*cm)
            intro_img.hAlign = 'CENTER'
            content.append(intro_img)
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    intro_text = """
    <b>¡Bienvenido a la era de la planificación financiera inteligente!</b><br/><br/>
    En un mundo donde el tiempo es el activo más valioso, <i>Tu Retiro Seguro</i> es la herramienta 
    definitiva para transformar tus sueños de jubilación en realidad tangible. No es solo una aplicación 
    de finanzas; es tu compañero estratégico hacia la libertad financiera.<br/><br/>
    <b>Dato importante:</b> El 78% de personas mayores de 65 años dependen únicamente de su pensión. 
    Sin planificación adecuada, muchos enfrentan dificultades económicas. Nuestra plataforma cambia esta realidad.
    """
    content.append(Paragraph(intro_text, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("🎯 ¿QUÉ ES TU RETIRO SEGURO?", subsection_style))

    features_data = [
        ['🧮', '<b>Matemáticas Financieras</b>', 'Algoritmos de valor del dinero en el tiempo'],
        ['🤖', '<b>Inteligencia Artificial</b>', 'Análisis predictivo para escenarios futuros'],
        ['🎨', '<b>Experiencia Premium</b>', 'Interfaz intuitiva sin conocimientos técnicos'],
        ['🎮', '<b>Gamificación</b>', 'Aprendizaje con recompensas y logros'],
        ['👥', '<b>Comunidad</b>', 'Aprendizaje colaborativo con otros usuarios'],
    ]
    
    for icon, title, desc in features_data:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(Spacer(1, 0.5*cm))
    content.append(Paragraph("🌟 BENEFICIOS CLAVE", subsection_style))

    benefits = [
        ('💡', 'Visión Clara', 'Conoce exactamente cuánto capital acumularás con el tiempo'),
        ('🎯', 'Decisiones Inteligentes', 'Compara escenarios ilimitados para optimizar tu estrategia'),
        ('⏰', 'Ahorro de Tiempo', 'Calcula en segundos análisis que antes tomaban horas'),
        ('📈', 'Maximiza Rendimientos', 'Descubre las mejores oportunidades para tu perfil'),
        ('🛡️', 'Seguridad Financiera', 'Planifica con confianza y elimina incertidumbre'),
        ('📱', 'Acceso Universal', 'Disponible en cualquier dispositivo, 24/7'),
    ]

    for icon, title, desc in benefits:
        content.append(crear_caja_info(icon, title, desc, COLOR_EXITO))
        content.append(Spacer(1, 0.3*cm))

    content.append(PageBreak())

    # ==================== CAPÍTULO 2: PRIMEROS PASOS ====================
    content.append(Paragraph("🚀 2. PRIMEROS PASOS", section_style))
    content.append(Spacer(1, 0.5*cm))

    steps_img_path = os.path.join(images_dir, 'formulario_captura.png')
    if os.path.exists(steps_img_path):
        try:
            steps_img = Image(steps_img_path, width=14*cm, height=7*cm)
            steps_img.hAlign = 'CENTER'
            content.append(steps_img)
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    welcome = """
    <b>¡Tu aventura financiera comienza aquí!</b><br/><br/>
    Proceso de incorporación tan simple que estarás creando tu primera simulación en menos de 5 minutos. 
    Olvídate de la complejidad técnica; enfócate en construir tu futuro.
    """
    content.append(Paragraph(welcome, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("📋 GUÍA RÁPIDA", subsection_style))

    steps_data = [
        ['1', '🌐 Acceso', 'Abre la aplicación en tu navegador'],
        ['2', '👤 Registro', 'Crea cuenta o usa modo anónimo'],
        ['3', '🎯 Módulo', 'Selecciona Cartera, Jubilación o Bonos'],
        ['4', '📝 Datos', 'Ingresa tu información financiera'],
        ['5', '⚡ Calcula', 'Obtén resultados instantáneos'],
        ['6', '📊 Analiza', 'Explora gráficos y escenarios'],
        ['7', '💾 Guarda', 'Conserva tu historial de simulaciones'],
    ]
    
    steps_table = Table(steps_data, colWidths=[1.5*cm, 4.5*cm, 10*cm])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), COLOR_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (0, -1), 18),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (1, 0), (-1, -1), COLOR_FONDO),
        ('TEXTCOLOR', (1, 0), (-1, -1), COLOR_TEXTO),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (1, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_PRINCIPAL),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    content.append(steps_table)
    content.append(Spacer(1, 0.5*cm))

    tip_data = [[Paragraph(
        '<b>💡 Tip Profesional:</b> Comienza con el Módulo A (Crecimiento de Cartera) para establecer '
        'tu base financiera. Luego podrás proyectar tu jubilación con precisión.',
        ParagraphStyle('tip', fontSize=11, leading=16, textColor=COLOR_TEXTO)
    )]]
    
    tip_table = Table(tip_data, colWidths=[16*cm])
    tip_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#f59e0b')),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    content.append(tip_table)

    content.append(PageBreak())

    # ==================== CAPÍTULO 3: SISTEMA DE USUARIOS ====================
    content.append(Paragraph("👤 3. SISTEMA DE USUARIOS Y PERFILES", section_style))
    content.append(Spacer(1, 0.5*cm))

    user_text = """
    <b>Tu Identidad Financiera Personal</b><br/><br/>
    Sistema de perfiles que se adapta a tu estilo de planificación, guardando preferencias y 
    manteniendo historial completo de tu evolución financiera.
    """
    content.append(Paragraph(user_text, normal_style))
    content.append(Spacer(1, 0.5*cm))

    user_options = [
        ('👤', 'Usuario Anónimo', 'Acceso inmediato sin registro - ideal para explorar'),
        ('🔒', 'Cuenta Registrada', 'Perfil completo con historial permanente'),
        ('🎨', 'Personalización', 'Adapta la interfaz a tu gusto personal'),
        ('📱', 'Sincronización', 'Accede desde cualquier dispositivo'),
    ]

    for icon, title, desc in user_options:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(PageBreak())

    # ==================== CAPÍTULO 4: MÓDULO A ====================
    content.append(Paragraph("💼 4. MÓDULO A: CRECIMIENTO DE CARTERA", section_style))
    content.append(Spacer(1, 0.5*cm))

    modulo_a_img = os.path.join(images_dir, 'modulo_a_resultados.png')
    if os.path.exists(modulo_a_img):
        try:
            img_a = Image(modulo_a_img, width=15*cm, height=9*cm)
            img_a.hAlign = 'CENTER'
            content.append(img_a)
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    modulo_a_intro = """
    <b>El Fundamento de Tu Libertad Financiera</b><br/><br/>
    Ve exactamente cómo tu dinero crece con el tiempo, considerando aportes y el poder del interés compuesto. 
    Transforma números abstractos en una narrativa visual de tu futuro.
    """
    content.append(Paragraph(modulo_a_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("🎯 CARACTERÍSTICAS", subsection_style))

    modulo_a_feat = [
        ('📈', 'Visualización', 'Ve cómo crece tu capital con el tiempo'),
        ('⏰', 'Planificación', 'Define horizontes por edad o años'),
        ('💰', 'Optimización', 'Descubre aportes necesarios para tus metas'),
        ('📊', 'Comparación', 'Compara diferentes estrategias'),
        ('🎪', 'Interés Compuesto', 'Experimenta su poder de forma interactiva'),
    ]

    for icon, title, desc in modulo_a_feat:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(Spacer(1, 0.5*cm))
    content.append(Paragraph("📝 PARÁMETROS DE ENTRADA", subsection_style))

    params_a = [
        ['🎂 Edad Actual', 'Tu punto de partida (18-100 años)'],
        ['💵 Capital Inicial', 'Dinero disponible para invertir'],
        ['📅 Aportes Periódicos', 'Cuánto ahorras regularmente'],
        ['🔄 Frecuencia', 'Semanal, Mensual o Anual'],
        ['🎯 Meta de Edad', 'Edad objetivo para tu meta'],
        ['📈 TEA Esperada', 'Rendimiento anual esperado (3-15%)'],
    ]
    
    params_table = Table(params_a, colWidths=[6*cm, 10*cm])
    params_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), COLOR_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('BACKGROUND', (1, 0), (1, -1), COLOR_FONDO),
        ('TEXTCOLOR', (1, 0), (1, -1), COLOR_TEXTO),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_PRINCIPAL),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    content.append(params_table)

    content.append(PageBreak())

    # ==================== CAPÍTULO 5: MÓDULO B ====================
    content.append(Paragraph("🏖️ 5. MÓDULO B: PROYECCIÓN DE JUBILACIÓN", section_style))
    content.append(Spacer(1, 0.5*cm))

    modulo_b_img = os.path.join(images_dir, 'modulo_b_captura.png')
    if os.path.exists(modulo_b_img):
        try:
            img_b = Image(modulo_b_img, width=15*cm, height=9*cm)
            img_b.hAlign = 'CENTER'
            content.append(img_b)
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    modulo_b_intro = """
    <b>Tu Puente Hacia la Jubilación Soñada</b><br/><br/>
    ¿Cuánto dinero mensual necesitarás? ¿Cuántos años de ingresos pasivos? Responde estas preguntas 
    críticas con precisión matemática y escenarios realistas.
    """
    content.append(Paragraph(modulo_b_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("🌅 BENEFICIOS", subsection_style))

    modulo_b_feat = [
        ('💰', 'Pensión Mensual', 'Conoce exactamente cuánto recibirás cada mes'),
        ('📅', 'Duración del Retiro', 'Calcula cuánto durarán tus ahorros'),
        ('🏦', 'Optimización Fiscal', 'Compara regímenes tributarios'),
        ('🎭', 'Escenarios Múltiples', 'Explora diferentes estilos de retiro'),
        ('🔄', 'Ajustes Automáticos', 'Considera inflación en proyecciones'),
    ]

    for icon, title, desc in modulo_b_feat:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(Spacer(1, 0.5*cm))
    content.append(Paragraph("⚙️ CONFIGURACIÓN", subsection_style))

    params_b = [
        ['💼 Tipo de Retiro', 'Pensión mensual o retiro total'],
        ['📊 Régimen Tributario', 'Impuestos locales vs extranjeros'],
        ['⏳ Años de Jubilación', 'Duración de ingresos pasivos (20-40 años)'],
        ['📈 TEA de Retiro', 'Rendimiento durante jubilación (3-5%)'],
        ['🏠 Estilo de Vida', 'Nivel de gastos mensual deseado'],
    ]
    
    params_table_b = Table(params_b, colWidths=[6*cm, 10*cm])
    params_table_b.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), COLOR_SECUNDARIO),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('BACKGROUND', (1, 0), (1, -1), COLOR_FONDO),
        ('TEXTCOLOR', (1, 0), (1, -1), COLOR_TEXTO),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_SECUNDARIO),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    content.append(params_table_b)

    content.append(PageBreak())

    # ==================== CAPÍTULO 6: MÓDULO C ====================
    content.append(Paragraph("📈 6. MÓDULO C: VALORACIÓN DE BONOS", section_style))
    content.append(Spacer(1, 0.5*cm))

    modulo_c_img = os.path.join(images_dir, 'modulo_c_captura.png')
    if os.path.exists(modulo_c_img):
        try:
            img_c = Image(modulo_c_img, width=15*cm, height=9*cm)
            img_c.hAlign = 'CENTER'
            content.append(img_c)
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    modulo_c_intro = """
    <b>Domina el Arte de la Inversión en Bonos</b><br/><br/>
    Los bonos son inversiones seguras del mercado. Este módulo te enseña a evaluar cualquier bono 
    con precisión profesional, determinando si es una oportunidad atractiva.
    """
    content.append(Paragraph(modulo_c_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("💎 VENTAJAS", subsection_style))

    modulo_c_feat = [
        ('🔍', 'Análisis Profesional', 'Metodología de bancos de inversión'),
        ('📊', 'Valor Presente', 'Calcula el precio justo de bonos'),
        ('🎯', 'Decisiones Inteligentes', 'Identifica si está sobrevalorado o es ganga'),
        ('📈', 'Comparación', 'Evalúa diferentes bonos en misma escala'),
        ('🛡️', 'Gestión de Riesgos', 'Entiende riesgo de crédito y duración'),
    ]

    for icon, title, desc in modulo_c_feat:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(Spacer(1, 0.5*cm))
    content.append(Paragraph("📋 PARÁMETROS DEL BONO", subsection_style))

    params_c = [
        ['💵 Valor Nominal', 'Valor que paga al vencimiento ($1,000 típico)'],
        ['🎟️ Tasa Cupón', 'Interés anual que paga el bono'],
        ['📅 Frecuencia de Pago', 'Cada cuánto se pagan intereses'],
        ['⏰ Plazo', 'Años restantes hasta pago final (1-30)'],
        ['📊 TEA de Mercado', 'Rendimiento requerido por inversionistas'],
    ]
    
    params_table_c = Table(params_c, colWidths=[6*cm, 10*cm])
    params_table_c.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), COLOR_ACENTO),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('BACKGROUND', (1, 0), (1, -1), COLOR_FONDO),
        ('TEXTCOLOR', (1, 0), (1, -1), COLOR_TEXTO),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_ACENTO),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    content.append(params_table_c)

    content.append(PageBreak())

    # ==================== CAPÍTULO 7: ESCENARIOS ====================
    content.append(Paragraph("🎲 7. ANÁLISIS DE ESCENARIOS AVANZADOS", section_style))
    content.append(Spacer(1, 0.5*cm))

    escenarios_intro = """
    <b>La Diferencia Entre Soñar y Planificar</b><br/><br/>
    ¿Qué pasa si las tasas cambian? ¿Y si te jubilas antes? ¿Cómo afecta la inflación? 
    Nuestros escenarios responden con análisis probabilísticos y visualizaciones.
    """
    content.append(Paragraph(escenarios_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("🔮 ESCENARIOS DISPONIBLES", subsection_style))

    escenarios = [
        ('📈', 'Sensibilidad de Tasas', 'Impacto de cambios del 1% en TEA'),
        ('🏖️', 'Jubilación Anticipada', 'Efecto de jubilarte 5 años antes'),
        ('💸', 'Inflación Variable', 'Diferentes tasas de inflación'),
        ('🎯', 'Análisis Probabilístico', 'Probabilidad de éxito de tu plan'),
        ('🔄', 'Escenarios Combinados', 'Múltiples variables simultáneas'),
    ]

    for icon, title, desc in escenarios:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(PageBreak())

    # ==================== CAPÍTULO 8: GAMIFICACIÓN ====================
    content.append(Paragraph("📊 8. SISTEMA DE LOGROS Y GAMIFICACIÓN", section_style))
    content.append(Spacer(1, 0.5*cm))

    gamification_img = os.path.join(images_dir, 'logros_captura.png')
    if os.path.exists(gamification_img):
        try:
            img_gam = Image(gamification_img, width=14*cm, height=8*cm)
            img_gam.hAlign = 'CENTER'
            content.append(img_gam)
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    gam_intro = """
    <b>¡Convierte el Aprendizaje en una Aventura!</b><br/><br/>
    Nuestro sistema de gamificación transforma cada paso en una experiencia motivadora que 
    te mantiene enganchado con tus objetivos financieros.
    """
    content.append(Paragraph(gam_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("🏆 LOGROS DESBLOQUEABLES", subsection_style))

    achievements = [
        ('🎯', 'Primer Cálculo', 'Tu primera simulación - ¡el comienzo!'),
        ('📈', 'Analista Experto', '10 simulaciones completadas'),
        ('💎', 'Planificador Maestro', '50 simulaciones - eres estratega'),
        ('👥', 'Comparador Social', 'Explora comparaciones con otros'),
        ('🎪', 'Coleccionista', '3 logros obtenidos - ¡vas bien!'),
        ('👑', 'Maestro Financiero', 'Todos los logros - ¡eres experto!'),
    ]

    for icon, title, desc in achievements:
        content.append(crear_caja_info(icon, title, desc, COLOR_EXITO))
        content.append(Spacer(1, 0.3*cm))

    content.append(Spacer(1, 0.5*cm))

    why_works = """
    <b>¿Por qué funciona?</b> La ciencia del comportamiento demuestra que recompensas frecuentes 
    mantienen la motivación a largo plazo. Cada logro valida tu progreso y enseña conceptos 
    financieros de manera natural y memorable.
    """
    content.append(Paragraph(why_works, normal_style))

    content.append(PageBreak())

    # ==================== CAPÍTULO 9: COMPARACIÓN SOCIAL ====================
    content.append(Paragraph("👥 9. COMPARACIÓN SOCIAL INTELIGENTE", section_style))
    content.append(Spacer(1, 0.5*cm))

    social_intro = """
    <b>Aprende de la Comunidad</b><br/><br/>
    La planificación financiera no es solitaria. Compara tus estrategias con usuarios similares, 
    aprende de sus éxitos y ajusta tus planes con datos reales.
    """
    content.append(Paragraph(social_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("🔍 COMPARACIONES DISPONIBLES", subsection_style))

    social_features = [
        ('📊', 'Perfil Demográfico', 'Compara con personas de tu edad'),
        ('💰', 'Estrategias de Ahorro', 'Cómo otros alcanzan sus metas'),
        ('🎯', 'Rendimientos', 'Aprende de estrategias exitosas'),
        ('📈', 'Progreso Temporal', 'Evolución de la comunidad'),
        ('💡', 'Lecciones Aprendidas', 'Experiencia colectiva'),
    ]

    for icon, title, desc in social_features:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(PageBreak())

    # ==================== CAPÍTULO 10: MARKETPLACE ====================
    content.append(Paragraph("🛒 10. MARKETPLACE DE TEMPLATES", section_style))
    content.append(Spacer(1, 0.5*cm))

    marketplace_intro = """
    <b>Biblioteca de Estrategias Financieras</b><br/><br/>
    ¿Por qué reinventar? Accede a configuraciones profesionales creadas por expertos y 
    usuarios exitosos. Aprende de las mejores estrategias probadas.
    """
    content.append(Paragraph(marketplace_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("📚 TEMPLATES DISPONIBLES", subsection_style))

    templates = [
        ('💼', 'Conservador Seguro', 'Minimiza riesgos, asegura estabilidad'),
        ('📈', 'Crecimiento Agresivo', 'Maximiza rendimientos a largo plazo'),
        ('🏖️', 'Jubilación Temprana', 'Planes FIRE (Financial Independence)'),
        ('👨‍👩‍👧‍👦', 'Familia Joven', 'Optimizado para familias con hijos'),
        ('🏠', 'Propietario', 'Incluye inversiones inmobiliarias'),
        ('🎓', 'Profesional', 'Para altos ingresos y objetivos ambiciosos'),
    ]

    for icon, title, desc in templates:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(PageBreak())

    # ==================== CAPÍTULO 11: REPORTES ====================
    content.append(Paragraph("📄 11. REPORTES PROFESIONALES EN PDF", section_style))
    content.append(Spacer(1, 0.5*cm))

    reports_intro = """
    <b>Documentos que Impresionan</b><br/><br/>
    Transforma tus simulaciones en documentos elegantes y completos que puedes compartir 
    con asesores, familiares o mantener como registro personal.
    """
    content.append(Paragraph(reports_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("📋 CONTENIDO DE REPORTES", subsection_style))

    report_features = [
        ('📊', 'Resumen Ejecutivo', 'Números clave en un vistazo'),
        ('📈', 'Gráficos Profesionales', 'Visualizaciones impactantes'),
        ('📝', 'Parámetros Detallados', 'Todos los inputs utilizados'),
        ('💰', 'Proyecciones', 'Tablas completas de crecimiento'),
        ('🏷️', 'Metadatos', 'Fecha, hora y versión de simulación'),
        ('🎨', 'Diseño Elegante', 'Formato profesional para compartir'),
    ]

    for icon, title, desc in report_features:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(PageBreak())

    # ==================== CAPÍTULO 12: SOPORTE ====================
    content.append(Paragraph("🔧 12. SOPORTE Y SOLUCIÓN DE PROBLEMAS", section_style))
    content.append(Spacer(1, 0.5*cm))

    support_intro = """
    <b>Soporte que Nunca te Deja Solo</b><br/><br/>
    Sistema de soporte integral que te acompaña en cada paso de tu viaje financiero. 
    Aquí encuentras soluciones a los problemas más comunes.
    """
    content.append(Paragraph(support_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("🆘 SOLUCIONES RÁPIDAS", subsection_style))

    solutions = [
        ('🌐', 'Problemas de Conexión', 'Verifica internet y navegador actualizado'),
        ('📱', 'Visualización', 'Asegura que JavaScript esté habilitado'),
        ('📊', 'Resultados Inesperados', 'Revisa rangos realistas de TEA (3-15%)'),
        ('💾', 'Problemas de Guardado', 'Inicia sesión para funciones completas'),
        ('📄', 'PDF no Descarga', 'Permite descargas emergentes en navegador'),
        ('🎯', 'Dudas Conceptuales', 'Consulta nuestro glosario integrado'),
    ]

    for icon, title, desc in solutions:
        content.append(crear_caja_info(icon, title, desc))
        content.append(Spacer(1, 0.3*cm))

    content.append(Spacer(1, 0.5*cm))

    contact_box = [[Paragraph(
        '<b>📞 Contacto y Asistencia:</b><br/><br/>'
        '📧 Email: soporte@turetiroseguro.com<br/>'
        '🌐 Web: www.turetiroseguro.com<br/>'
        '⏰ Disponibilidad: 24/7 online<br/>'
        '📱 Aplicación web sin instalación requerida',
        normal_style
    )]]
    
    contact_table = Table(contact_box, colWidths=[16*cm])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_FONDO),
        ('BOX', (0, 0), (-1, -1), 2, COLOR_PRINCIPAL),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    content.append(contact_table)

    content.append(PageBreak())

    # ==================== CAPÍTULO 13: GLOSARIO ====================
    content.append(Paragraph("📚 13. GLOSARIO EJECUTIVO", section_style))
    content.append(Spacer(1, 0.5*cm))

    glossary_intro = """
    <b>Tu Diccionario Personal de Finanzas</b><br/><br/>
    Términos importantes del mundo financiero explicados de manera simple y directa. 
    Elimina la jerga técnica y domina los conceptos clave.
    """
    content.append(Paragraph(glossary_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("🔤 TÉRMINOS ESENCIALES", subsection_style))

    glossary_data = [
        ['<b>Término</b>', '<b>Definición</b>'],
        ['TEA', 'Tasa Efectiva Anual - Rendimiento real anual considerando capitalización'],
        ['Interés Compuesto', '"Interés sobre interés" - El secreto de la riqueza a largo plazo'],
        ['Valor del Tiempo', 'Un dólar hoy vale más que un dólar mañana'],
        ['Valor Presente', 'Conversión de valores futuros a su equivalente actual'],
        ['Valor Nominal', 'Valor facial o de vencimiento de un instrumento'],
        ['Tasa Cupón', 'Interés que pagan los bonos periódicamente'],
        ['Duration', 'Sensibilidad de un bono a cambios en tasas'],
        ['Riesgo de Crédito', 'Probabilidad de incumplimiento del emisor'],
        ['Rentabilidad Esperada', 'Rendimiento promedio anticipado de inversión'],
        ['Diversificación', 'No poner todos los huevos en una canasta'],
        ['Capitalización', 'Reinversión de ganancias para generar más ganancias'],
        ['Horizonte Temporal', 'Período de tiempo de tu inversión'],
        ['Liquidez', 'Facilidad para convertir activo en efectivo'],
        ['Volatilidad', 'Grado de variación en rendimientos'],
        ['Portafolio', 'Conjunto de inversiones diversificadas'],
    ]
    
    glossary_table = Table(glossary_data, colWidths=[4*cm, 12*cm])
    glossary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRINCIPAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLOR_TEXTO),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_PRINCIPAL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_FONDO, colors.white]),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(glossary_table)

    content.append(PageBreak())

    # ==================== CIERRE INSPIRACIONAL ====================
    content.append(Spacer(1, 2*cm))
    
    closing_title = Paragraph(
        "🎯 ¡TU FUTURO FINANCIERO COMIENZA HOY!",
        ParagraphStyle('closing_title', fontSize=22, alignment=TA_CENTER, 
                      textColor=COLOR_PRINCIPAL, fontName='Helvetica-Bold', leading=28)
    )
    content.append(closing_title)
    content.append(Spacer(1, 1*cm))

    closing_text = """
    Has completado la lectura de este manual, pero este es solo el principio de tu viaje hacia 
    la libertad financiera. Cada simulación que realices, cada logro que desbloquees, cada 
    estrategia que compares te acerca un paso más a tus sueños.<br/><br/>

    <i>Recuerda: el conocimiento financiero no es un lujo, es una necesidad. Y ahora tienes 
    la herramienta más poderosa para adquirir ese conocimiento.</i><br/><br/>

    <b>El mejor momento para planificar tu futuro fue hace 10 años. El segundo mejor momento es ahora.</b><br/><br/>

    ¡Que tu viaje hacia la prosperidad financiera sea extraordinario!
    """
    content.append(Paragraph(closing_text, normal_style))
    content.append(Spacer(1, 1*cm))

    # Footer con información adicional
    footer_data = [[Paragraph(
        '<b>Tu Retiro Seguro</b> - Simulador Financiero Inteligente<br/>'
        'Desarrollado por: Unidad II - Finanzas Corporativas<br/>'
        'Manual de Usuario v2.0 - Noviembre 2025<br/><br/>'
        '© 2025 Todos los derechos reservados',
        ParagraphStyle('footer', fontSize=9, alignment=TA_CENTER, textColor=colors.grey, leading=12)
    )]]
    
    footer_table = Table(footer_data, colWidths=[16*cm])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_FONDO),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    content.append(footer_table)

    # Generar PDF
    try:
        doc.build(content)
        print(f"✅ Manual de usuario creado exitosamente en: {filename}")
        print(f"📁 Coloca las imágenes en: {images_dir}")
        print("\n📸 Imágenes recomendadas:")
        print("   - logo_universidad.png (Logo de tu universidad)")
        print("   - dashboard_principal.png (Captura del dashboard)")
        print("   - modulo_a_captura.png (Captura Módulo A)")
        print("   - modulo_a_resultados.png (Resultados Módulo A)")
        print("   - modulo_b_captura.png (Captura Módulo B)")
        print("   - modulo_c_captura.png (Captura Módulo C)")
        print("   - formulario_captura.png (Captura de formulario)")
        print("   - logros_captura.png (Captura de logros)")
        return filename
    except Exception as e:
        print(f"❌ Error al generar PDF: {str(e)}")
        return None

if __name__ == "__main__":
    crear_manual_usuario()