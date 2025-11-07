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

    modulo_b_text = """
    Este módulo utiliza los resultados del Módulo A para calcular su pensión mensual
    al momento de la jubilación, considerando impuestos y diferentes opciones de retiro.
    """

    content.append(Paragraph(modulo_b_text, normal_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Campos del formulario:", section_style))

    campos_b_data = [
        ["Tipo de Retiro", "Pensión mensual o cobro total", "Obligatorio"],
        ["Tipo de Impuesto", "29.5% extranjero o 5% local", "Obligatorio"],
        ["Años de Retiro", "Duración estimada del retiro", "Obligatorio para pensión"],
        ["TEA de Retiro", "Tasa durante el retiro", "Opcional"]
    ]

    campos_b_table = Table(campos_b_data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
    campos_b_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    content.append(campos_b_table)

    content.append(PageBreak())

    # 7. Módulo C: Valoración de Bonos
    content.append(Paragraph("7. Módulo C: Valoración de Bonos", subtitle_style))
    content.append(Spacer(1, 15))

    modulo_c_text = """
    Este módulo calcula el valor presente de un bono basado en sus características
    y la tasa de retorno esperada del inversionista.
    """

    content.append(Paragraph(modulo_c_text, normal_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Campos del formulario:", section_style))

    campos_c_data = [
        ["Valor Nominal", "Valor facial del bono en USD", "Obligatorio"],
        ["Tasa Cupón", "Tasa de interés del cupón (TEA %)", "Obligatorio"],
        ["Frecuencia de Pago", "Periodicidad de pagos de cupón", "Obligatorio"],
        ["Plazo al Vencimiento", "Años hasta el vencimiento", "Obligatorio"],
        ["TEA de Retorno", "Tasa esperada por el inversionista", "Obligatorio"]
    ]

    campos_c_table = Table(campos_c_data, colWidths=[1.8*inch, 2.8*inch, 1.2*inch])
    campos_c_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    content.append(campos_c_table)

    content.append(PageBreak())

    # 8. Interpretación de Resultados
    content.append(Paragraph("8. Interpretación de Resultados", subtitle_style))
    content.append(Spacer(1, 15))

    interpretacion_text = """
    Los resultados se presentan en tarjetas resumen y gráficos interactivos.
    Todos los valores están en dólares estadounidenses (USD) y se redondean a dos decimales.

    <b>Capital Final:</b> Monto total acumulado al final del período de inversión.
    <b>Aportes Totales:</b> Suma de todos los aportes realizados (inicial + periódicos).
    <b>Ganancia Bruta:</b> Interés generado por el capital (Capital Final - Aportes Totales).
    <b>Rentabilidad Total:</b> Porcentaje de ganancia sobre los aportes totales.
    """

    content.append(Paragraph(interpretacion_text, normal_style))

    content.append(PageBreak())

    # 9. Exportación de Reportes
    content.append(Paragraph("9. Exportación de Reportes", subtitle_style))
    content.append(Spacer(1, 15))

    export_text = """
    Cada módulo incluye un botón "Descargar Reporte PDF" que genera un documento
    profesional con:

    • Parámetros de entrada utilizados
    • Resultados detallados
    • Gráficos (cuando aplique)
    • Tablas de amortización
    • Fecha y hora de generación
    """

    content.append(Paragraph(export_text, normal_style))

    content.append(PageBreak())

    # 10. Solución de Problemas
    content.append(Paragraph("10. Solución de Problemas", subtitle_style))
    content.append(Spacer(1, 15))

    problemas_data = [
        ["Problema", "Solución"],
        ["La aplicación no carga", "Verifique su conexión a internet y navegador"],
        ["Errores de cálculo", "Revise que todos los campos obligatorios estén completos"],
        ["PDF no se descarga", "Permita descargas en su navegador"],
        ["Gráficos no aparecen", "Asegúrese de que JavaScript esté habilitado"],
        ["Valores no realistas", "Verifique rangos de TEA (típicamente 3-15%)"]
    ]

    problemas_table = Table(problemas_data, colWidths=[2*inch, 4*inch])
    problemas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    content.append(problemas_table)

    content.append(PageBreak())

    # 11. Glosario
    content.append(Paragraph("11. Glosario", subtitle_style))
    content.append(Spacer(1, 15))

    glosario_data = [
        ["TEA", "Tasa Efectiva Anual - Rendimiento real anual de una inversión"],
        ["Interés Compuesto", "Interés que se calcula sobre el capital inicial más intereses acumulados"],
        ["Valor Presente", "Valor actual de un flujo futuro de dinero"],
        ["Valor Nominal", "Valor facial o de vencimiento de un bono"],
        ["Tasa Cupón", "Tasa de interés que paga un bono periódicamente"],
        ["PDF", "Portable Document Format - Formato estándar para documentos"]
    ]

    glosario_table = Table(glosario_data, colWidths=[1.5*inch, 4.5*inch])
    glosario_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    content.append(glosario_table)

    # Generar PDF
    doc.build(content)
    return filename

if __name__ == "__main__":
    crear_manual_usuario()
    print("Manual de usuario creado exitosamente")
