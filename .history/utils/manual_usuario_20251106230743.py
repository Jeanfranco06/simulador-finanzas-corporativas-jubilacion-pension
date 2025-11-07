from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, ListFlowable, ListItem
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

def crear_manual_usuario():
    """Crear manual de usuario atractivo y persuasivo en PDF"""

    # Crear directorio si no existe
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'docs')
    os.makedirs(output_dir, exist_ok=True)

    # Ruta del archivo
    filename = os.path.join(output_dir, 'manual_usuario.pdf')

    # Crear documento
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()

    # Estilos personalizados con formato APA
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=40,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0ea5e9'),
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=20,
        spaceAfter=25,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica-Bold'
    )

    section_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading3'],
        fontSize=16,
        spaceAfter=18,
        textColor=colors.HexColor('#0ea5e9'),
        fontName='Helvetica-Bold'
    )

    subsection_style = ParagraphStyle(
        'CustomSubsection',
        parent=styles['Heading4'],
        fontSize=14,
        spaceAfter=15,
        textColor=colors.HexColor('#475569'),
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=14,
        alignment=TA_JUSTIFY,
        lineHeight=1.4
    )

    highlight_style = ParagraphStyle(
        'HighlightStyle',
        parent=styles['Normal'],
        fontSize=13,
        spaceAfter=16,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#0ea5e9'),
        fontName='Helvetica-Bold',
        lineHeight=1.5
    )

    benefit_style = ParagraphStyle(
        'BenefitStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#059669'),
        lineHeight=1.3
    )

    # Contenido del manual
    content = []

    # Portada atractiva
    content.append(Paragraph("💰 TU RETIRO SEGURO", title_style))
    content.append(Paragraph("La Revolución en Planificación Financiera Personal", subtitle_style))
    content.append(Spacer(1, 60))

    # Información de publicación (formato APA)
    publication_info = """
    <b>Manual del Usuario</b><br/>
    <i>Simulador Financiero de Jubilación</i><br/>
    Versión 2.0 Profesional<br/>
    Noviembre 2025<br/>
    <br/>
    <b>Desarrollado por:</b> Unidad II - Finanzas Corporativas<br/>
    <b>Plataforma:</b> Aplicación Web Profesional<br/>
    <b>Público Objetivo:</b> Planificadores Financieros Personales
    """
    content.append(Paragraph(publication_info, normal_style))
    content.append(Spacer(1, 80))

    # Cita inspiracional
    inspirational_quote = """
    <i>"El futuro pertenece a quienes creen en la belleza de sus sueños"</i><br/>
    — Eleanor Roosevelt
    """
    content.append(Paragraph(inspirational_quote, highlight_style))

    content.append(PageBreak())

    # Índice ejecutivo
    content.append(Paragraph("📋 ÍNDICE EJECUTIVO", subtitle_style))
    content.append(Spacer(1, 20))

    indice_data = [
        ["🎯", "Introducción y Beneficios Clave", "3"],
        ["🚀", "Primeros Pasos - Comienza Tu Viaje", "5"],
        ["👤", "Sistema de Usuarios y Perfiles", "7"],
        ["💼", "Módulo A: Crecimiento de Cartera", "9"],
        ["🏖️", "Módulo B: Proyección de Jubilación", "13"],
        ["📈", "Módulo C: Valoración de Bonos", "17"],
        ["🎲", "Análisis de Escenarios Avanzados", "21"],
        ["📊", "Sistema de Logros y Gamificación", "25"],
        ["👥", "Comparación Social Inteligente", "27"],
        ["🛒", "Marketplace de Templates", "29"],
        ["📄", "Reportes Profesionales en PDF", "31"],
        ["🔧", "Soporte y Solución de Problemas", "33"],
        ["📚", "Glosario Ejecutivo", "35"]
    ]

    indice_table = Table(indice_data, colWidths=[0.4*inch, 3.8*inch, 0.5*inch])
    indice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f9ff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0c4a6e')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bae6fd'))
    ]))
    content.append(indice_table)

    content.append(PageBreak())

    # 1. Introducción y Beneficios Clave
    content.append(Paragraph("🎯 1. INTRODUCCIÓN Y BENEFICIOS CLAVE", subtitle_style))
    content.append(Spacer(1, 20))

    intro_text = """
    <b>¡Bienvenido a la era de la planificación financiera inteligente!</b><br/><br/>

    En un mundo donde el tiempo es el activo más valioso, <i>Tu Retiro Seguro</i> emerge como la herramienta definitiva
    para transformar tus sueños de jubilación en realidad tangible. Esta no es solo una aplicación más de finanzas;
    es tu compañero estratégico en el viaje hacia la libertad financiera.
    """

    content.append(Paragraph(intro_text, normal_style))

    content.append(Paragraph("🌟 <b>BENEFICIOS TRANSFORMADORES QUE CAMBIARÁN TU VIDA:</b>", highlight_style))

    benefits = [
        "💡 <b>Visión Clara del Futuro:</b> Conoce exactamente cuánto capital acumularás y cómo crecerá tu dinero con el tiempo",
        "🎯 <b>Decisiones Inteligentes:</b> Compara escenarios ilimitados para optimizar tu estrategia de inversión",
        "⏰ <b>Ahorro de Tiempo:</b> Calcula en segundos lo que antes tomaba horas de análisis complejo",
        "📈 <b>Maximización de Rendimientos:</b> Descubre las mejores oportunidades de inversión para tu perfil",
        "🛡️ <b>Seguridad Financiera:</b> Planifica tu jubilación con confianza y elimina la incertidumbre",
        "🎮 <b>Experiencia Gamificada:</b> Aprende finanzas mientras te diviertes con nuestro sistema de logros",
        "👥 <b>Aprendizaje Social:</b> Comparte conocimientos y aprende de la comunidad financiera",
        "📱 <b>Acceso Universal:</b> Usa desde cualquier dispositivo, en cualquier momento y lugar"
    ]

    for benefit in benefits:
        content.append(Paragraph(benefit, benefit_style))

    content.append(Spacer(1, 20))

    value_prop = """
    <b>¿Por qué elegir Tu Retiro Seguro?</b><br/><br/>

    Mientras otros te ofrecen datos fríos y fórmulas complejas, nosotros te entregamos <i>conocimiento accionable</i>
    que transforma tu realidad financiera. Nuestra plataforma combina la precisión matemática de las finanzas corporativas
    con una experiencia de usuario intuitiva y motivadora.
    """

    content.append(Paragraph(value_prop, normal_style))

    content.append(PageBreak())

    # 2. Primeros Pasos
    content.append(Paragraph("🚀 2. PRIMEROS PASOS - COMIENZA TU VIAJE", subtitle_style))
    content.append(Spacer(1, 20))

    welcome_text = """
    <b>¡Tu aventura financiera comienza aquí!</b><br/><br/>

    Hemos diseñado un proceso de incorporación tan simple que podrás estar creando tu primera simulación
    financiera en menos de 5 minutos. Olvídate de la complejidad técnica; enfócate en construir tu futuro.
    """

    content.append(Paragraph(welcome_text, normal_style))

    content.append(Paragraph("📋 <b>PASOS PARA COMENZAR:</b>", highlight_style))

    steps = [
        "🌐 <b>Acceso Instantáneo:</b> Abre tu navegador y visita la aplicación (no requiere instalación)",
        "👤 <b>Elige Tu Experiencia:</b> Regístrate para guardar simulaciones o continúa como usuario anónimo",
        "🎯 <b>Selecciona Tu Módulo:</b> Elige entre Crecimiento de Cartera, Jubilación o Valoración de Bonos",
        "📝 <b>Ingresa Tus Datos:</b> Completa el formulario intuitivo con información personalizada",
        "⚡ <b>Calcula al Instante:</b> Obtén resultados profesionales en tiempo real",
        "📊 <b>Analiza y Compara:</b> Explora gráficos interactivos y escenarios alternativos",
        "💾 <b>Guarda Tu Progreso:</b> Mantén un registro de todas tus simulaciones y estrategias"
    ]

    for step in steps:
        content.append(Paragraph(step, benefit_style))

    content.append(Spacer(1, 20))

    tip_text = """
    <b>💡 Tip Profesional:</b> Comienza con el Módulo A (Crecimiento de Cartera) para establecer
    tu base financiera. Una vez que tengas claridad sobre tu capacidad de ahorro, podrás
    proyectar con precisión tu jubilación ideal.
    """

    content.append(Paragraph(tip_text, highlight_style))

    content.append(PageBreak())

    # 3. Sistema de Usuarios y Perfiles
    content.append(Paragraph("👤 3. SISTEMA DE USUARIOS Y PERFILES", subtitle_style))
    content.append(Spacer(1, 20))

    user_system_text = """
    <b>Tu Identidad Financiera Personal</b><br/><br/>

    En Tu Retiro Seguro, entendemos que cada persona es única. Por eso hemos creado un sistema
    de perfiles que se adapta a tu estilo de planificación financiera, guardando tus preferencias
    y manteniendo un historial completo de tu evolución financiera.
    """

    content.append(Paragraph(user_system_text, normal_style))

    content.append(Paragraph("🔐 <b>OPCIONES DE ACCESO FLEXIBLES:</b>", highlight_style))

    user_options = [
        "👤 <b>Usuario Anónimo:</b> Acceso inmediato sin registro - perfecto para explorar y experimentar",
        "🔒 <b>Cuenta Registrada:</b> Perfil completo con historial permanente y funciones avanzadas",
        "🎨 <b>Personalización:</b> Adapta colores, idioma y preferencias a tu gusto personal",
        "📱 <b>Sincronización:</b> Accede desde cualquier dispositivo manteniendo tu progreso"
    ]

    for option in user_options:
        content.append(Paragraph(option, benefit_style))

    content.append(Paragraph("🏆 <b>SISTEMA DE LOGROS MOTIVACIONAL:</b>", highlight_style))

    achievements_desc = """
    <b>¡Convierte el aprendizaje financiero en una aventura!</b><br/><br/>

    Nuestro sistema de gamificación te recompensa por cada paso que das hacia la libertad financiera.
    Desde tu primera simulación hasta estrategias complejas, cada logro desbloquea nuevos conocimientos
    y mantiene viva tu motivación para seguir aprendiendo.
    """

    content.append(Paragraph(achievements_desc, normal_style))

    content.append(PageBreak())

    # 4. Módulo A: Crecimiento de Cartera
    content.append(Paragraph("💼 4. MÓDULO A: CRECIMIENTO DE CARTERA", subtitle_style))
    content.append(Spacer(1, 20))

    modulo_a_intro = """
    <b>El Fundamento de Tu Libertad Financiera</b><br/><br/>

    Imagina poder ver exactamente cómo tu dinero crece con el tiempo, considerando cada aporte
    que haces y el poder mágico del interés compuesto. Este módulo transforma números abstractos
    en una narrativa visual de tu futuro financiero.
    """

    content.append(Paragraph(modulo_a_intro, normal_style))

    content.append(Paragraph("🎯 <b>¿QUÉ LOGRARÁS CON ESTE MÓDULO?</b>", highlight_style))

    modulo_a_benefits = [
        "📈 <b>Visualización del Crecimiento:</b> Ve cómo $1,000 hoy pueden convertirse en $10,000+ en el futuro",
        "⏰ <b>Planificación Temporal:</b> Define horizontes de inversión personalizados por edad o años",
        "💰 <b>Optimización de Aportes:</b> Descubre cuánto necesitas ahorrar mensualmente para alcanzar tus metas",
        "📊 <b>Análisis Comparativo:</b> Compara diferentes estrategias de ahorro e inversión",
        "🎪 <b>Efecto Compuesto:</b> Experimenta el poder del interés compuesto de manera interactiva"
    ]

    for benefit in modulo_a_benefits:
        content.append(Paragraph(benefit, benefit_style))

    content.append(Paragraph("📝 <b>CAMPOS DE CONFIGURACIÓN INTUITIVOS:</b>", subsection_style))

    campos_a_data = [
        ["🎂 <b>Edad Actual</b>", "Tu punto de partida en el viaje financiero", "18-100 años"],
        ["💵 <b>Capital Inicial</b>", "Dinero que ya tienes disponible para invertir", "Opcional"],
        ["📅 <b>Aportes Periódicos</b>", "Cuánto puedes ahorrar regularmente", "Personalizable"],
        ["🔄 <b>Frecuencia</b>", "Cada cuánto realizas tus aportes", "Semanal/Mensual/Anual"],
        ["🎯 <b>Meta de Edad</b>", "Edad objetivo para alcanzar tu meta financiera", "Flexible"],
        ["📈 <b>TEA Esperada</b>", "Rendimiento anual esperado de tus inversiones", "3-15% típico"]
    ]

    campos_a_table = Table(campos_a_data, colWidths=[1.8*inch, 3.2*inch, 1.5*inch])
    campos_a_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0fdf4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#166534')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bbf7d0'))
    ]))
    content.append(campos_a_table)

    content.append(PageBreak())

    # 5. Módulo B: Proyección de Jubilación
    content.append(Paragraph("🏖️ 5. MÓDULO B: PROYECCIÓN DE JUBILACIÓN", subtitle_style))
    content.append(Spacer(1, 20))

    modulo_b_intro = """
    <b>Tu Puente Hacia la Jubilación Soñada</b><br/><br/>

    ¿Cuánto dinero mensual necesitarás para mantener tu estilo de vida actual durante la jubilación?
    ¿Cuántos años podrás disfrutar de ingresos pasivos? Este módulo responde estas preguntas críticas
    con precisión matemática y escenarios realistas.
    """

    content.append(Paragraph(modulo_b_intro, normal_style))

    content.append(Paragraph("🌅 <b>VISUALIZA TU FUTURO IDEAL:</b>", highlight_style))

    modulo_b_benefits = [
        "💰 <b>Pensión Mensual Clara:</b> Conoce exactamente cuánto recibirás cada mes en tu jubilación",
        "📅 <b>Duración del Retiro:</b> Calcula cuánto tiempo durarán tus ahorros con diferentes escenarios",
        "🏦 <b>Optimización Fiscal:</b> Compara regímenes tributarios para maximizar tus ingresos",
        "🎭 <b>Escenarios Múltiples:</b> Explora diferentes estilos de retiro y sus implicaciones",
        "🔄 <b>Ajustes Automáticos:</b> Considera incrementos por inflación en tus proyecciones"
    ]

    for benefit in modulo_b_benefits:
        content.append(Paragraph(benefit, benefit_style))

    content.append(Paragraph("⚙️ <b>CONFIGURACIÓN PERSONALIZADA:</b>", subsection_style))

    campos_b_data = [
        ["💼 <b>Tipo de Retiro</b>", "Pensión mensual o retiro total", "Estrategia personal"],
        ["📊 <b>Régimen Tributario</b>", "Impuestos locales vs extranjeros", "Optimización fiscal"],
        ["⏳ <b>Años de Jubilación</b>", "Duración estimada de ingresos pasivos", "20-40 años típico"],
        ["📈 <b>TEA de Retiro</b>", "Rendimiento durante la jubilación", "Conservador: 3-5%"],
        ["🏠 <b>Estilo de Vida</b>", "Nivel de gastos mensual deseado", "Personalizable"]
    ]

    campos_b_table = Table(campos_b_data, colWidths=[1.8*inch, 3.2*inch, 1.5*inch])
    campos_b_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fef3c7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#92400e')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fde68a'))
    ]))
    content.append(campos_b_table)

    content.append(PageBreak())

    # 6. Módulo C: Valoración de Bonos
    content.append(Paragraph("📈 6. MÓDULO C: VALORACIÓN DE BONOS", subtitle_style))
    content.append(Spacer(1, 20))

    modulo_c_intro = """
    <b>Domina el Arte de la Inversión en Bonos</b><br/><br/>

    Los bonos representan una de las inversiones más seguras del mercado. Este módulo te enseña
    a evaluar cualquier bono con precisión profesional, determinando si representa una oportunidad
    de inversión atractiva o si debes buscar alternativas.
    """

    content.append(Paragraph(modulo_c_intro, normal_style))

    content.append(Paragraph("💎 <b>VENTAJAS COMPETITIVAS ÚNICAS:</b>", highlight_style))

    modulo_c_benefits = [
        "🔍 <b>Análisis Profesional:</b> Evalúa bonos con la misma metodología que usan los bancos de inversión",
        "📊 <b>Valor Presente Preciso:</b> Calcula el precio justo de cualquier instrumento de deuda",
        "🎯 <b>Decisiones Inteligentes:</b> Determina si un bono está sobrevalorado o es una ganga",
        "📈 <b>Comparación de Rendimientos:</b> Evalúa diferentes bonos en una misma escala",
        "🛡️ <b>Gestión de Riesgos:</b> Entiende el riesgo de crédito y duración de tus inversiones"
    ]

    for benefit in modulo_c_benefits:
        content.append(Paragraph(benefit, benefit_style))

    content.append(Paragraph("📋 <b>CARACTERÍSTICAS DEL BONO A EVALUAR:</b>", subsection_style))

    campos_c_data = [
        ["💵 <b>Valor Nominal</b>", "Valor facial que el emisor pagará al vencimiento", "$1,000 típico"],
        ["🎟️ <b>Tasa Cupón</b>", "Interés anual que paga el bono", "Variable por emisor"],
        ["📅 <b>Frecuencia de Pago</b>", "Cada cuánto se pagan los intereses", "Anual/Semestral"],
        ["⏰ <b>Plazo al Vencimiento</b>", "Años restantes hasta el pago final", "1-30 años"],
        ["📊 <b>TEA de Mercado</b>", "Rendimiento requerido por los inversionistas", "Basado en riesgo"]
    ]

    campos_c_table = Table(campos_c_data, colWidths=[1.8*inch, 3.2*inch, 1.5*inch])
    campos_c_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e0f2fe')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0c4a6e')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bae6fd'))
    ]))
    content.append(campos_c_table)

    content.append(PageBreak())

    # 7. Análisis de Escenarios Avanzados
    content.append(Paragraph("🎲 7. ANÁLISIS DE ESCENARIOS AVANZADOS", subtitle_style))
    content.append(Spacer(1, 20))

    escenarios_intro = """
    <b>La Diferencia Entre Soñar y Planificar</b><br/><br/>

    ¿Qué sucede si las tasas de interés cambian? ¿Y si decides jubilarte antes de lo planeado?
    ¿Cómo afecta la inflación a tus ahorros? Nuestros escenarios avanzados responden estas
    preguntas críticas con análisis probabilísticos y visualizaciones impactantes.
    """

    content.append(Paragraph(escenarios_intro, normal_style))

    content.append(Paragraph("🔮 <b>ESCENARIOS INTELIGENTES QUE TRANSFORMAN TU PLANIFICACIÓN:</b>", highlight_style))

    escenarios_benefits = [
        "📈 <b>Sensibilidad de Tasas:</b> Descubre cómo cambios del 1% en TEA afectan tus resultados",
        "🏖️ <b>Jubilación Anticipada:</b> Evalúa el impacto de jubilarte 5 años antes de lo planeado",
        "💸 <b>Inflación Variable:</b> Simula escenarios con diferentes tasas de inflación",
        "🎯 <b>Análisis Probabilístico:</b> Entiende la probabilidad de éxito de tu plan financiero",
        "🔄 <b>Escenarios Combinados:</b> Combina múltiples variables para análisis complejos"
    ]

    for benefit in escenarios_benefits:
        content.append(Paragraph(benefit, benefit_style))

    content.append(PageBreak())

    # 8. Sistema de Logros y Gamificación
    content.append(Paragraph("📊 8. SISTEMA DE LOGROS Y GAMIFICACIÓN", subtitle_style))
    content.append(Spacer(1, 20))

    gamification_intro = """
    <b>¡Convierte el Aprendizaje Financiero en una Aventura!</b><br/><br/>

    Olvídate de los libros de finanzas aburridos y las fórmulas complejas. Nuestro sistema de
    gamificación transforma cada paso de tu aprendizaje financiero en una experiencia motivadora
    y gratificante que te mantiene enganchado con tus objetivos.
    """

    content.append(Paragraph(gamification_intro, normal_style))

    content.append(Paragraph("🏆 <b>LOGROS QUE DESBLOQUEAN TU POTENCIAL:</b>", highlight_style))

    achievements_list = [
        "🎯 <b>Primer Cálculo:</b> Tu primera simulación financiera - ¡el comienzo de todo!",
        "📈 <b>Analista Experto:</b> 10 simulaciones completadas - dominas los conceptos básicos",
        "💎 <b>Planificador Maestro:</b> 50 simulaciones - eres un estratega financiero",
        "👥 <b>Comparador Social:</b> Explora cómo te comparas con otros planificadores",
        "🎪 <b>Coleccionista de Logros:</b> 3 logros obtenidos - ¡vas por el camino correcto!",
        "👑 <b>Maestro de Finanzas:</b> Todos los logros desbloqueados - ¡eres un experto!"
    ]

    for achievement in achievements_list:
        content.append(Paragraph(achievement, benefit_style))

    content.append(Spacer(1, 20))

    gamification_value = """
    <b>¿Por qué funciona la gamificación?</b><br/><br/>

    La ciencia del comportamiento demuestra que las recompensas frecuentes mantienen la motivación
    a largo plazo. Cada logro que desbloqueas no solo valida tu progreso, sino que también te
    enseña conceptos financieros de manera natural y memorable.
    """

    content.append(Paragraph(gamification_value, normal_style))

    content.append(PageBreak())

    # 9. Comparación Social Inteligente
    content.append(Paragraph("👥 9. COMPARACIÓN SOCIAL INTELIGENTE", subtitle_style))
    content.append(Spacer(1, 20))

    social_intro = """
    <b>Aprende de la Comunidad, Crece con los Mejores</b><br/><br/>

    La planificación financiera no es un viaje solitario. Nuestra plataforma inteligente te permite
    comparar tus estrategias con usuarios similares, aprender de sus éxitos y ajustar tus planes
    basándote en datos reales de la comunidad.
    """

    content.append(Paragraph(social_intro, normal_style))

    content.append(Paragraph("🔍 <b>COMPARACIONES QUE TE AYUDAN A CRECER:</b>", highlight_style))

    social_features = [
        "📊 <b>Perfil Demográfico:</b> Compara con personas de tu edad y situación similar",
        "💰 <b>Estrategias de Ahorro:</b> Descubre cómo otros alcanzan sus metas financieras",
        "🎯 <b>Rendimientos Obtenidos:</b> Aprende de estrategias que han funcionado para otros",
        "📈 <b>Progreso Temporal:</b> Ve cómo evoluciona la comunidad financiera con el tiempo",
        "💡 <b>Lecciones Aprendidas:</b> Benefíciate de la experiencia colectiva de la comunidad"
    ]

    for feature in social_features:
        content.append(Paragraph(feature, benefit_style))

    content.append(PageBreak())

    # 10. Marketplace de Templates
    content.append(Paragraph("🛒 10. MARKETPLACE DE TEMPLATES", subtitle_style))
    content.append(Spacer(1, 20))

    marketplace_intro = """
    <b>La Biblioteca de Estrategias Financieras Más Completa</b><br/><br/>

    ¿Por qué reinventar la rueda cuando puedes aprender de las mejores estrategias ya probadas?
    Nuestro marketplace de templates te da acceso a configuraciones profesionales creadas por
    expertos y otros usuarios exitosos.
    """

    content.append(Paragraph(marketplace_intro, normal_style))

    content.append(Paragraph("📚 <b>TEMPLATES QUE ACELERAN TU APRENDIZAJE:</b>", highlight_style))

    templates = [
        "💼 <b>Conservador Seguro:</b> Estrategias para minimizar riesgos y asegurar estabilidad",
        "📈 <b>Crecimiento Agresivo:</b> Configuraciones para maximizar rendimientos a largo plazo",
        "🏖️ <b>Jubilación Temprana:</b> Planes específicos para FIRE (Financial Independence, Retire Early)",
        "👨‍👩‍👧‍👦 <b>Familia Joven:</b> Estrategias optimizadas para familias con hijos",
        "🏠 <b>Propietario:</b> Planes que incluyen inversiones inmobiliarias",
        "🎓 <b>Profesional:</b> Configuraciones para altos ingresos con objetivos ambiciosos"
    ]

    for template in templates:
        content.append(Paragraph(template, benefit_style))

    content.append(PageBreak())

    # 11. Reportes Profesionales en PDF
    content.append(Paragraph("📄 11. REPORTES PROFESIONALES EN PDF", subtitle_style))
    content.append(Spacer(1, 20))

    reports_intro = """
    <b>Documentos Profesionales que Impresionan</b><br/><br/>

    Tus análisis financieros merecen ser presentados con el profesionalismo que se merecen.
    Nuestros reportes PDF transforman tus simulaciones en documentos elegantes y completos
    que puedes compartir con asesores, familiares o mantener como registro personal.
    """

    content.append(Paragraph(reports_intro, normal_style))

    content.append(Paragraph("📋 <b>CONTENIDO COMPLETO DE TUS REPORTES:</b>", highlight_style))

    report_features = [
        "📊 <b>Resumen Ejecutivo:</b> Los números clave en un vistazo",
        "📈 <b>Gráficos Profesionales:</b> Visualizaciones impactantes de tus resultados",
        "📝 <b>Parámetros Detallados:</b> Todos los inputs que utilizaste",
        "💰 <b>Proyecciones Financieras:</b> Tablas completas de crecimiento proyectado",
        "🏷️ <b>Metadatos Completos:</b> Fecha, hora y versión de la simulación",
        "🎨 <b>Diseño Elegante:</b> Formato profesional listo para compartir"
    ]

    for feature in report_features:
        content.append(Paragraph(feature, benefit_style))

    content.append(PageBreak())

    # 12. Soporte y Solución de Problemas
    content.append(Paragraph("🔧 12. SOPORTE Y SOLUCIÓN DE PROBLEMAS", subtitle_style))
    content.append(Spacer(1, 20))

    support_intro = """
    <b>Soporte Técnico que Nunca te Deja Solo</b><br/><br/>

    Entendemos que la planificación financiera puede ser compleja, por eso hemos diseñado
    un sistema de soporte integral que te acompaña en cada paso de tu viaje financiero.
    """

    content.append(Paragraph(support_intro, normal_style))

    content.append(Paragraph("🆘 <b>SOLUCIONES PARA PROBLEMAS COMUNES:</b>", highlight_style))

    support_solutions = [
        "🌐 <b>Problemas de Conexión:</b> Verifica tu conexión a internet y navegador actualizado",
        "📱 <b>Problemas de Visualización:</b> Asegura que JavaScript esté habilitado",
        "📊 <b>Resultados Inesperados:</b> Revisa rangos realistas de TEA (3-15%)",
        "💾 <b>Problemas de Guardado:</b> Inicia sesión para acceder a funciones completas",
        "📄 <b>PDF no Descarga:</b> Permite descargas emergentes en tu navegador",
        "🎯 <b>Dudas Conceptuales:</b> Consulta nuestro glosario integrado"
    ]

    for solution in support_solutions:
        content.append(Paragraph(solution, benefit_style))

    content.append(PageBreak())

    # 13. Glosario Ejecutivo
    content.append(Paragraph("📚 13. GLOSARIO EJECUTIVO", subtitle_style))
    content.append(Spacer(1, 20))

    glossary_intro = """
    <b>Tu Diccionario Personal de Finanzas</b><br/><br/>

    Hemos compilado los términos más importantes del mundo financiero en un glosario
    accesible que elimina la jerga técnica y explica conceptos complejos de manera
    simple y directa.
    """

    content.append(Paragraph(glossary_intro, normal_style))

    content.append(Paragraph("🔤 <b>TÉRMINOS ESENCIALES PARA TU ÉXITO FINANCIERO:</b>", highlight_style))

    glossary_terms = [
