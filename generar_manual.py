"""
Script para generar el Manual de Usuario del Simulador Financiero
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime


def generar_manual_usuario():
    """Genera el manual de usuario en PDF"""
    
    # Crear documento
    doc = SimpleDocTemplate(
        "docs/Manual_Usuario.pdf",
        pagesize=letter,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=1*inch,
        rightMargin=1*inch
    )
    
    # Estilos
    estilos = getSampleStyleSheet()
    
    estilo_titulo = ParagraphStyle(
        'TituloPortada',
        parent=estilos['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    estilo_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=estilos['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2e5c9a'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    estilo_seccion = ParagraphStyle(
        'Seccion',
        parent=estilos['Heading3'],
        fontSize=13,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    estilo_normal = ParagraphStyle(
        'NormalJustificado',
        parent=estilos['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    estilo_lista = ParagraphStyle(
        'Lista',
        parent=estilos['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6
    )
    
    # Contenido del manual
    story = []
    
    # ==================== PORTADA ====================
    story.append(Spacer(1, 2*inch))
    
    titulo = Paragraph("MANUAL DE USUARIO", estilo_titulo)
    story.append(titulo)
    story.append(Spacer(1, 0.3*inch))
    
    subtitulo = Paragraph("Simulador Financiero de Jubilación", estilo_subtitulo)
    story.append(subtitulo)
    story.append(Spacer(1, 0.5*inch))
    
    version = Paragraph("Versión 1.0", estilo_normal)
    version.alignment = TA_CENTER
    story.append(version)
    story.append(Spacer(1, 0.2*inch))
    
    fecha = Paragraph(f"{datetime.now().strftime('%B %Y')}", estilo_normal)
    fecha.alignment = TA_CENTER
    story.append(fecha)
    
    story.append(PageBreak())
    
    # ==================== ÍNDICE ====================
    story.append(Paragraph("ÍNDICE", estilo_titulo))
    story.append(Spacer(1, 0.3*inch))
    
    indices = [
        "1. Introducción",
        "2. Requisitos del Sistema",
        "3. Instalación",
        "4. Inicio de la Aplicación",
        "5. Interfaz Principal",
        "6. Módulo A: Crecimiento de Cartera",
        "7. Módulo B: Proyección de Jubilación",
        "8. Módulo C: Valoración de Bonos",
        "9. Exportación de Resultados",
        "10. Preguntas Frecuentes",
        "11. Soporte y Contacto"
    ]
    
    for indice in indices:
        story.append(Paragraph(indice, estilo_lista))
    
    story.append(PageBreak())
    
    # ==================== 1. INTRODUCCIÓN ====================
    story.append(Paragraph("1. INTRODUCCIÓN", estilo_subtitulo))
    
    texto = """
    Bienvenido al Simulador Financiero de Jubilación, una herramienta profesional diseñada para 
    ayudarle a planificar su futuro financiero. Este software le permite simular el crecimiento 
    de su cartera de inversión, calcular su pensión mensual estimada y valorar bonos de manera 
    precisa y sencilla.
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Paragraph("1.1 Características Principales", estilo_seccion))
    
    caracteristicas = [
        "• <b>Módulo A - Crecimiento de Cartera:</b> Simula cómo crece su capital con aportes periódicos e interés compuesto.",
        "• <b>Módulo B - Proyección de Jubilación:</b> Calcula su pensión mensual considerando impuestos y diferentes escenarios.",
        "• <b>Módulo C - Valoración de Bonos:</b> Determina el valor presente de bonos con cupones periódicos.",
        "• <b>Gráficas Interactivas:</b> Visualice la evolución de su patrimonio de forma clara.",
        "• <b>Exportación a PDF:</b> Genere reportes profesionales de todos sus cálculos.",
        "• <b>Validaciones Automáticas:</b> El sistema valida todos los datos ingresados."
    ]
    
    for item in caracteristicas:
        story.append(Paragraph(item, estilo_lista))
    
    story.append(PageBreak())
    
    # ==================== 2. REQUISITOS DEL SISTEMA ====================
    story.append(Paragraph("2. REQUISITOS DEL SISTEMA", estilo_subtitulo))
    
    texto = """
    Para ejecutar correctamente el Simulador Financiero, su computadora debe cumplir con los 
    siguientes requisitos mínimos:
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Paragraph("2.1 Requisitos de Hardware", estilo_seccion))
    
    hardware = [
        "• Procesador: Intel Core i3 o equivalente (mínimo)",
        "• Memoria RAM: 4 GB (mínimo), 8 GB (recomendado)",
        "• Espacio en disco: 500 MB disponibles",
        "• Pantalla: Resolución mínima de 1280x720 píxeles"
    ]
    
    for item in hardware:
        story.append(Paragraph(item, estilo_lista))
    
    story.append(Paragraph("2.2 Requisitos de Software", estilo_seccion))
    
    software = [
        "• Sistema Operativo: Windows 10/11, macOS 10.14+, o Linux Ubuntu 20.04+",
        "• Python 3.8 o superior (si ejecuta desde código fuente)",
        "• Navegador web: Chrome, Firefox, Safari o Edge (última versión)"
    ]
    
    for item in software:
        story.append(Paragraph(item, estilo_lista))
    
    story.append(PageBreak())
    
    # ==================== 3. INSTALACIÓN ====================
    story.append(Paragraph("3. INSTALACIÓN", estilo_subtitulo))
    
    story.append(Paragraph("3.1 Instalación desde Código Fuente", estilo_seccion))
    
    texto = """
    Si recibió el proyecto como código fuente, siga estos pasos para instalarlo:
    """
    story.append(Paragraph(texto, estilo_normal))
    
    pasos_instalacion = [
        "<b>Paso 1:</b> Descomprima el archivo ZIP en una carpeta de su elección.",
        "<b>Paso 2:</b> Abra una terminal o línea de comandos.",
        "<b>Paso 3:</b> Navegue hasta la carpeta del proyecto usando el comando 'cd'.",
        "<b>Paso 4:</b> Instale las dependencias ejecutando: <b>pip install -r requirements.txt</b>",
        "<b>Paso 5:</b> Espere a que se instalen todas las librerías necesarias."
    ]
    
    for paso in pasos_instalacion:
        story.append(Paragraph(paso, estilo_lista))
        story.append(Spacer(1, 6))
    
    story.append(PageBreak())
    
    # ==================== 4. INICIO DE LA APLICACIÓN ====================
    story.append(Paragraph("4. INICIO DE LA APLICACIÓN", estilo_subtitulo))
    
    texto = """
    Una vez instalada la aplicación, puede iniciarla de la siguiente manera:
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Paragraph("4.1 Desde Código Fuente", estilo_seccion))
    
    pasos_inicio = [
        "<b>Paso 1:</b> Abra una terminal en la carpeta del proyecto.",
        "<b>Paso 2:</b> Ejecute el comando: <b>streamlit run app.py</b>",
        "<b>Paso 3:</b> Se abrirá automáticamente una ventana en su navegador con la aplicación.",
        "<b>Paso 4:</b> Si no se abre automáticamente, acceda manualmente a: http://localhost:8501"
    ]
    
    for paso in pasos_inicio:
        story.append(Paragraph(paso, estilo_lista))
        story.append(Spacer(1, 6))
    
    story.append(Paragraph("4.2 Cierre de la Aplicación", estilo_seccion))
    
    texto = """
    Para cerrar la aplicación, simplemente cierre la ventana del navegador y presione 
    Ctrl+C en la terminal donde se está ejecutando.
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(PageBreak())
    
    # ==================== 5. INTERFAZ PRINCIPAL ====================
    story.append(Paragraph("5. INTERFAZ PRINCIPAL", estilo_subtitulo))
    
    texto = """
    La interfaz del Simulador Financiero está organizada en pestañas para facilitar su uso:
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Paragraph("5.1 Componentes de la Interfaz", estilo_seccion))
    
    componentes = [
        "• <b>Barra Lateral (Sidebar):</b> Contiene información general y ayuda contextual.",
        "• <b>Pestaña Inicio:</b> Pantalla de bienvenida con instrucciones generales.",
        "• <b>Pestaña Módulo A:</b> Simulación de crecimiento de cartera.",
        "• <b>Pestaña Módulo B:</b> Proyección de jubilación y pensión mensual.",
        "• <b>Pestaña Módulo C:</b> Valoración de bonos.",
        "• <b>Iconos de Ayuda (?):</b> Disponibles en cada campo para información adicional."
    ]
    
    for comp in componentes:
        story.append(Paragraph(comp, estilo_lista))
    
    story.append(PageBreak())
    
    # ==================== 6. MÓDULO A ====================
    story.append(Paragraph("6. MÓDULO A: CRECIMIENTO DE CARTERA", estilo_subtitulo))
    
    texto = """
    Este módulo le permite simular cómo crecerá su capital a lo largo del tiempo considerando 
    aportes periódicos e interés compuesto.
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Paragraph("6.1 Datos Requeridos", estilo_seccion))
    
    datos = [
        "• <b>Edad Actual:</b> Su edad en años (entre 18 y 100).",
        "• <b>Monto Inicial:</b> Capital inicial disponible en dólares (USD).",
        "• <b>Aporte Periódico:</b> Cantidad que aportará regularmente en USD.",
        "• <b>Frecuencia de Aportes:</b> Mensual, Bimestral, Trimestral, Cuatrimestral, Semestral o Anual.",
        "• <b>Plazo:</b> Puede especificarlo en años o mediante la edad de jubilación.",
        "• <b>Tasa Efectiva Anual (TEA):</b> Rendimiento anual esperado entre 0% y 50%."
    ]
    
    for dato in datos:
        story.append(Paragraph(dato, estilo_lista))
    
    story.append(Paragraph("6.2 Procedimiento", estilo_seccion))
    
    procedimiento = [
        "<b>1.</b> Complete todos los campos del formulario.",
        "<b>2.</b> Verifique que los valores sean correctos.",
        "<b>3.</b> Haga clic en el botón 'Calcular Proyección'.",
        "<b>4.</b> Revise los resultados mostrados en pantalla.",
        "<b>5.</b> Explore la gráfica interactiva de crecimiento.",
        "<b>6.</b> Si lo desea, exporte los resultados a PDF."
    ]
    
    for paso in procedimiento:
        story.append(Paragraph(paso, estilo_lista))
        story.append(Spacer(1, 4))
    
    story.append(Paragraph("6.3 Interpretación de Resultados", estilo_seccion))
    
    texto = """
    Los resultados le mostrarán:
    """
    story.append(Paragraph(texto, estilo_normal))
    
    resultados = [
        "• <b>Capital Final:</b> Monto total acumulado al final del periodo.",
        "• <b>Aportes Totales:</b> Suma de todos sus aportes.",
        "• <b>Ganancia Bruta:</b> Diferencia entre capital final y aportes.",
        "• <b>Rentabilidad:</b> Porcentaje de ganancia sobre los aportes.",
        "• <b>Gráfica:</b> Comparación visual entre aportes y saldo total.",
        "• <b>Tabla Detallada:</b> Desglose periodo por periodo."
    ]
    
    for resultado in resultados:
        story.append(Paragraph(resultado, estilo_lista))
    
    story.append(PageBreak())
    
    # ==================== 7. MÓDULO B ====================
    story.append(Paragraph("7. MÓDULO B: PROYECCIÓN DE JUBILACIÓN", estilo_subtitulo))
    
    texto = """
    Este módulo utiliza el capital acumulado del Módulo A para calcular su jubilación, 
    considerando impuestos y diferentes opciones de retiro.
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Paragraph("7.1 Requisito Previo", estilo_seccion))
    
    texto = """
    <b>Importante:</b> Debe completar primero el Módulo A para poder usar el Módulo B.
    """
    story.append(Paragraph(texto, estilo_lista))
    
    story.append(Paragraph("7.2 Opciones de Retiro", estilo_seccion))
    
    opciones = [
        "• <b>Cobro Total:</b> Retira todo el capital en un solo pago.",
        "• <b>Pensión Mensual:</b> Recibe pagos mensuales durante un periodo determinado."
    ]
    
    for opcion in opciones:
        story.append(Paragraph(opcion, estilo_lista))
    
    story.append(Paragraph("7.3 Consideraciones de Impuestos", estilo_seccion))
    
    texto = """
    El sistema calcula automáticamente los impuestos sobre sus ganancias:
    """
    story.append(Paragraph(texto, estilo_normal))
    
    impuestos = [
        "• <b>29.5% Fuente Extranjera:</b> Aplicable a inversiones en el exterior.",
        "• <b>5% Bolsa Local:</b> Aplicable a ganancias en bolsa peruana."
    ]
    
    for impuesto in impuestos:
        story.append(Paragraph(impuesto, estilo_lista))
    
    story.append(Paragraph("7.4 Procedimiento", estilo_seccion))
    
    procedimiento_b = [
        "<b>1.</b> Seleccione el tipo de retiro deseado.",
        "<b>2.</b> Elija el régimen tributario aplicable.",
        "<b>3.</b> Si elige pensión mensual, indique los años esperados de retiro.",
        "<b>4.</b> Opcionalmente, puede modificar la TEA durante el retiro.",
        "<b>5.</b> Haga clic en 'Calcular Jubilación'.",
        "<b>6.</b> Revise los resultados: impuestos, capital neto y pensión mensual."
    ]
    
    for paso in procedimiento_b:
        story.append(Paragraph(paso, estilo_lista))
        story.append(Spacer(1, 4))
    
    story.append(PageBreak())
    
    # ==================== 8. MÓDULO C ====================
    story.append(Paragraph("8. MÓDULO C: VALORACIÓN DE BONOS", estilo_subtitulo))
    
    texto = """
    Este módulo le permite calcular el valor presente de un bono considerando sus cupones 
    periódicos y tasa de retorno requerida.
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Paragraph("8.1 Datos Requeridos", estilo_seccion))
    
    datos_bono = [
        "• <b>Valor Nominal:</b> Valor par del bono en USD.",
        "• <b>Tasa Cupón Anual:</b> Porcentaje de cupón que paga el bono.",
        "• <b>Frecuencia de Pago:</b> Con qué periodicidad se pagan los cupones.",
        "• <b>Plazo al Vencimiento:</b> Años hasta que vence el bono.",
        "• <b>TEA Retorno Esperada:</b> Tasa de descuento o retorno requerido."
    ]
    
    for dato in datos_bono:
        story.append(Paragraph(dato, estilo_lista))
    
    story.append(Paragraph("8.2 Interpretación del Resultado", estilo_seccion))
    
    interpretacion = [
        "• <b>Valor Presente > Valor Nominal:</b> El bono cotiza con PRIMA (buen cupón).",
        "• <b>Valor Presente < Valor Nominal:</b> El bono cotiza con DESCUENTO (cupón bajo).",
        "• <b>Valor Presente = Valor Nominal:</b> El bono cotiza A LA PAR."
    ]
    
    for inter in interpretacion:
        story.append(Paragraph(inter, estilo_lista))
    
    story.append(PageBreak())
    
    # ==================== 9. EXPORTACIÓN ====================
    story.append(Paragraph("9. EXPORTACIÓN DE RESULTADOS", estilo_subtitulo))
    
    texto = """
    El sistema le permite exportar todos sus cálculos a archivos PDF profesionales.
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Paragraph("9.1 Cómo Exportar", estilo_seccion))
    
    pasos_export = [
        "<b>1.</b> Complete los cálculos en cualquier módulo.",
        "<b>2.</b> Localice el botón 'Exportar a PDF' en la parte inferior.",
        "<b>3.</b> Haga clic en el botón.",
        "<b>4.</b> Aparecerá un botón de descarga.",
        "<b>5.</b> Haga clic en 'Descargar PDF'.",
        "<b>6.</b> El archivo se guardará en su carpeta de descargas."
    ]
    
    for paso in pasos_export:
        story.append(Paragraph(paso, estilo_lista))
        story.append(Spacer(1, 4))
    
    story.append(Paragraph("9.2 Contenido del PDF", estilo_seccion))
    
    texto = """
    El PDF exportado incluye:
    """
    story.append(Paragraph(texto, estilo_normal))
    
    contenido_pdf = [
        "• Resumen ejecutivo de todos los cálculos",
        "• Gráficas de crecimiento y evolución",
        "• Tablas detalladas con todos los periodos",
        "• Fecha y hora de generación del reporte",
        "• Formato profesional listo para imprimir"
    ]
    
    for item in contenido_pdf:
        story.append(Paragraph("• " + item, estilo_lista))
    
    story.append(PageBreak())
    
    # ==================== 10. PREGUNTAS FRECUENTES ====================
    story.append(Paragraph("10. PREGUNTAS FRECUENTES", estilo_subtitulo))
    
    faqs = [
        ("<b>¿Puedo guardar mis cálculos?</b>", 
         "Sí, puede exportarlos a PDF. Actualmente no hay guardado automático en la aplicación."),
        
        ("<b>¿Los cálculos están garantizados?</b>", 
         "Los cálculos son proyecciones basadas en las tasas ingresadas. Los rendimientos reales pueden variar."),
        
        ("<b>¿Puedo usar otras monedas?</b>", 
         "El sistema está diseñado específicamente para dólares estadounidenses (USD)."),
        
        ("<b>¿Qué pasa si ingreso datos incorrectos?</b>", 
         "El sistema valida todos los datos y le mostrará mensajes de error claros si algo está incorrecto."),
        
        ("<b>¿Necesito conexión a Internet?</b>", 
         "No, una vez instalado, el sistema funciona completamente sin conexión."),
        
        ("<b>¿Puedo comparar escenarios?</b>", 
         "Sí, el Módulo B incluye un comparador de escenarios para diferentes edades y tasas.")
    ]
    
    for pregunta, respuesta in faqs:
        story.append(Paragraph(pregunta, estilo_seccion))
        story.append(Paragraph(respuesta, estilo_normal))
        story.append(Spacer(1, 10))
    
    story.append(PageBreak())
    
    # ==================== 11. SOPORTE ====================
    story.append(Paragraph("11. SOPORTE Y CONTACTO", estilo_subtitulo))
    
    texto = """
    Si tiene alguna duda o problema con el Simulador Financiero, puede contactarnos 
    a través de los siguientes medios:
    """
    story.append(Paragraph(texto, estilo_normal))
    
    story.append(Spacer(1, 0.3*inch))
    
    contacto = [
        "<b>Correo Electrónico:</b> soporte@simuladorfinanciero.com",
        "<b>Teléfono:</b> +51 (01) 123-4567",
        "<b>Horario de Atención:</b> Lunes a Viernes, 9:00 AM - 6:00 PM",
        "<b>Sitio Web:</b> www.simuladorfinanciero.com"
    ]
    
    for item in contacto:
        story.append(Paragraph(item, estilo_lista))
        story.append(Spacer(1, 8))
    
    story.append(Spacer(1, 0.5*inch))
    
    texto_final = """
    <b>Gracias por utilizar el Simulador Financiero de Jubilación.</b><br/>
    Esperamos que esta herramienta le sea de gran utilidad en la planificación de su futuro financiero.
    """
    story.append(Paragraph(texto_final, estilo_normal))
    
    story.append(Spacer(1, 1*inch))
    
    version_info = f"""
    <b>Versión:</b> 1.0<br/>
    <b>Fecha de Publicación:</b> {datetime.now().strftime('%B %Y')}<br/>
    <b>© 2025 Simulador Financiero. Todos los derechos reservados.</b>
    """
    story.append(Paragraph(version_info, estilo_lista))
    
    # Construir documento
    doc.build(story)
    print("✅ Manual de Usuario generado exitosamente: docs/Manual_Usuario.pdf")


if __name__ == "__main__":
    generar_manual_usuario()
