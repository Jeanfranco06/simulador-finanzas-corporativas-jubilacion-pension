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
    content.append(PageBreak())

    # 1. Introducción
    content.append(Paragraph("1. Introducción", subtitle_style))
    content.append(Spacer(1, 15))

    intro_text = """
    El Simulador Financiero de Jubilación es una herramienta profesional diseñada para ayudarle
    a planificar su futuro financiero. Esta aplicación integra conceptos avanzados de finanzas
    corporativas como el valor del dinero en el tiempo, interés compuesto, valoración de bonos
    y tasas equivalentes.

    La aplicación está dividida en tres módulos principales que le permiten:
    """

    content.append(Paragraph(intro_text, normal_style))

    features_data = [
        ["•", "Calcular el crecimiento de su capital con aportes periódicos"],
        ["•", "Proyectar su pensión mensual al momento de la jubilación"],
        ["•", "Valorar instrumentos de deuda (bonos)"],
        ["•", "Generar reportes detallados en formato PDF"],
        ["•", "Comparar diferentes escenarios de inversión"]
    ]

    features_table = Table(features_data, colWidths=[0.2*inch, 5*inch])
    features_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(features_table)

    content.append(PageBreak())

    # 2. Requisitos del Sistema
    content.append(Paragraph("2. Requisitos del Sistema", subtitle_style))
    content.append(Spacer(1, 15))

    req_data = [
        ["Navegador Web", "Google Chrome 90+, Firefox 88+, Safari 14+, Edge 90+"],
        ["Sistema Operativo", "Windows 10+, macOS 10.15+, Linux Ubuntu 18.04+"],
        ["Conexión a Internet", "Requerida para cargar la aplicación"],
        ["Resolución de Pantalla", "Mínimo 1024x768 píxeles"],
        ["JavaScript", "Habilitado en el navegador"]
    ]

    req_table = Table(req_data, colWidths=[2*inch, 4*inch])
    req_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    content.append(req_table)

    content.append(PageBreak())

    # 3. Instalación y Configuración
    content.append(Paragraph("3. Instalación y Configuración", subtitle_style))
    content.append(Spacer(1, 15))

    install_text = """
    La aplicación es completamente web-based, por lo que no requiere instalación.
    Simplemente acceda a la URL proporcionada por su institución educativa.

    Para un funcionamiento óptimo:
    """

    content.append(Paragraph(install_text, normal_style))

    config_data = [
        ["1.", "Asegúrese de tener una conexión a internet estable"],
        ["2.", "Utilice un navegador web moderno y actualizado"],
        ["3.", "Habilite JavaScript en su navegador"],
        ["4.", "Permita cookies si es necesario para la funcionalidad"]
    ]

    config_table = Table(config_data, colWidths=[0.3*inch, 5.5*inch])
    config_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    content.append(config_table)

    content.append(PageBreak())

    # 4. Primeros Pasos
    content.append(Paragraph("4. Primeros Pasos", subtitle_style))
    content.append(Spacer(1, 15))

    primeros_pasos = """
    Una vez que acceda a la aplicación, verá la página de inicio con información general
    sobre los módulos disponibles. Para comenzar:

    1. Navegue por la página de inicio para familiarizarse con las funcionalidades
    2. Seleccione el módulo que desea utilizar desde la barra de navegación
    3. Complete el formulario correspondiente con sus datos
    4. Haga clic en "Calcular" para obtener los resultados
    5. Analice los resultados y gráficos generados
    6. Exporte el reporte en PDF si lo desea
    """

    content.append(Paragraph(primeros_pasos, normal_style))

    content.append(PageBreak())

    # 5. Módulo A: Crecimiento de Cartera
    content.append(Paragraph("5. Módulo A: Crecimiento de Cartera", subtitle_style))
    content.append(Spacer(1, 15))

    modulo_a_text = """
    Este módulo calcula cómo crece su capital a lo largo del tiempo considerando
    aportes iniciales y periódicos, con el efecto del interés compuesto.
    """

    content.append(Paragraph(modulo_a_text, normal_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Campos del formulario:", section_style))

    campos_a_data = [
        ["Edad Actual", "Su edad actual (18-100 años)", "Obligatorio"],
        ["Monto Inicial", "Capital inicial en USD", "Opcional (mínimo $0)"],
        ["Aporte Periódico", "Monto que aporta regularmente en USD", "Opcional (mínimo $0)"],
        ["Frecuencia", "Periodicidad de los aportes", "Obligatorio"],
        ["Plazo", "Duración de la inversión (años o edad objetivo)", "Obligatorio"],
        ["TEA", "Tasa Efectiva Anual (%)", "Obligatorio (0-50%)"]
    ]

    campos_a_table = Table(campos_a_data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
    campos_a_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#334155')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0'))
    ]))
    content.append(campos_a_table)

    content.append(PageBreak())

    # 6. Módulo B: Proyección de Jubilación
    content.append(Paragraph("6. Módulo B: Proyección de Jubilación", subtitle_style))
    content.append(Spacer(1, 15))

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
