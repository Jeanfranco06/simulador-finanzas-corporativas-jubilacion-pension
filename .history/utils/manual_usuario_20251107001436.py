from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
import os

class NumberedCanvas(canvas.Canvas):
    """Canvas personalizado para agregar números de página"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        self.drawRightString(
            A4[0] - 2*cm,
            1.5*cm,
            f"Página {self._pageNumber} de {page_count}"
        )

def crear_manual_usuario():
    """Crear manual de usuario con diseño profesional tipo documento académico"""

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
        rightMargin=3*cm, 
        leftMargin=3*cm, 
        topMargin=2.5*cm, 
        bottomMargin=2.5*cm
    )

    # Colores corporativos elegantes
    COLOR_PRINCIPAL = colors.HexColor('#1e40af')  # Azul oscuro profesional
    COLOR_SECUNDARIO = colors.HexColor('#0891b2')  # Cyan oscuro
    COLOR_ACENTO = colors.HexColor('#7c3aed')  # Púrpura
    COLOR_TEXTO = colors.HexColor('#1e293b')  # Gris oscuro para texto
    COLOR_GRIS = colors.HexColor('#64748b')  # Gris medio

    # Estilos
    styles = getSampleStyleSheet()
    
    # Título principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=COLOR_PRINCIPAL,
        fontName='Helvetica-Bold',
        leading=34
    )

    # Subtítulo
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=COLOR_GRIS,
        fontName='Helvetica',
        leading=20
    )

    # Capítulo
    chapter_style = ParagraphStyle(
        'ChapterStyle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=16,
        spaceBefore=20,
        textColor=COLOR_PRINCIPAL,
        fontName='Helvetica-Bold',
        leading=22
    )

    # Sección
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=14,
        textColor=COLOR_SECUNDARIO,
        fontName='Helvetica-Bold',
        leading=18
    )

    # Subsección
    subsection_style = ParagraphStyle(
        'SubsectionStyle',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=10,
        textColor=COLOR_ACENTO,
        fontName='Helvetica-Bold',
        leading=15
    )

    # Texto normal
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=COLOR_TEXTO,
        leading=16,
        fontName='Helvetica'
    )

    # Texto destacado
    highlight_style = ParagraphStyle(
        'HighlightStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=10,
        alignment=TA_JUSTIFY,
        textColor=COLOR_TEXTO,
        fontName='Helvetica-Bold',
        leading=16
    )

    # Lista
    list_style = ParagraphStyle(
        'ListStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leftIndent=20,
        alignment=TA_JUSTIFY,
        textColor=COLOR_TEXTO,
        leading=15
    )

    # Pie de imagen
    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=10,
        alignment=TA_CENTER,
        textColor=COLOR_GRIS,
        fontName='Helvetica-Oblique',
        leading=12
    )

    content = []

    # ==================== PORTADA ====================
    
    # Logo universidad
    logo_path = os.path.join(images_dir, 'logount.png')
    if os.path.exists(logo_path):
        try:
            logo = Image(logo_path, width=7*cm, height=5*cm)
            logo.hAlign = 'CENTER'
            content.append(logo)
            content.append(Spacer(1, 1*cm))
        except:
            pass
    
    content.append(Paragraph("TU RETIRO SEGURO", title_style))
    content.append(Spacer(1, 0.3*cm))
    content.append(Paragraph("Manual de Usuario", subtitle_style))
    content.append(Paragraph("Simulador Financiero de Jubilación", subtitle_style))

    # Imagen principal
    dashboard_path = os.path.join(images_dir, 'dashboard_principal.jpeg')
    if os.path.exists(dashboard_path):
        try:
            dashboard = Image(dashboard_path, width=16*cm, height=9*cm)
            dashboard.hAlign = 'CENTER'
            content.append(dashboard)
            content.append(Spacer(1, 0.3*cm))
            content.append(Paragraph("Figura 1. Interfaz principal del simulador", caption_style))
        except:
            pass
    
    content.append(Spacer(1, 2*cm))

    # Información de publicación
    pub_text = """
    <b>Versión:</b> 2.0 Profesional<br/>
    <b>Fecha:</b> Noviembre 2025<br/>
    <b>Desarrollado para:</b> Unidad II - Finanzas Corporativas
    """
    content.append(Paragraph(pub_text, ParagraphStyle('pub', parent=normal_style, alignment=TA_CENTER)))
    content.append(Spacer(1, 1*cm))

    # Equipo
    team_text = """
    <b>Integrantes del Equipo:</b><br/>
    Gonzales Esquivel, Jeanfranco Jefferson<br/>
    Moreno Aguilar, Dalessandro Zahit<br/>
    Rodríguez Sandoval, Harry Sly<br/>
    Velásquez García, Ricardo Bernardo<br/>
    Carril Freyre, Justin Ismael Neil
    """
    content.append(Paragraph(team_text, ParagraphStyle('team', parent=normal_style, alignment=TA_CENTER, fontSize=10)))

    content.append(PageBreak())

    # ==================== ÍNDICE ====================
    content.append(Paragraph("ÍNDICE DE CONTENIDOS", chapter_style))
    content.append(Spacer(1, 0.5*cm))

    indice_items = [
        ("1.", "Introducción y Beneficios Clave", "3"),
        ("2.", "Primeros Pasos", "6"),
        ("3.", "Sistema de Usuarios y Perfiles", "8"),
        ("4.", "Módulo A: Crecimiento de Cartera de Inversión", "10"),
        ("5.", "Módulo B: Proyección de Jubilación", "13"),
        ("6.", "Módulo C: Valoración de Bonos", "16"),
        ("7.", "Análisis de Escenarios Avanzados", "19"),
        ("8.", "Sistema de Logros y Gamificación", "21"),
        ("9.", "Comparación Social Inteligente", "23"),
        ("10.", "Marketplace de Templates", "25"),
        ("11.", "Reportes Profesionales en PDF", "27"),
        ("12.", "Soporte y Solución de Problemas", "29"),
        ("13.", "Glosario de Términos Financieros", "31"),
    ]

    for num, titulo, pag in indice_items:
        line = f"{num} {titulo} {'.' * (80 - len(num) - len(titulo) - len(pag))} {pag}"
        content.append(Paragraph(line, list_style))

    content.append(PageBreak())

    # ==================== CAPÍTULO 1 ====================
    content.append(Paragraph("1. INTRODUCCIÓN Y BENEFICIOS CLAVE", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    intro_text = """
    Bienvenido a <b>Tu Retiro Seguro</b>, una plataforma tecnológica avanzada diseñada para 
    transformar la manera en que las personas planifican su futuro financiero. En un mundo donde 
    la incertidumbre económica es cada vez mayor, contar con herramientas profesionales para la 
    planificación de la jubilación se ha vuelto una necesidad fundamental.
    """
    content.append(Paragraph(intro_text, normal_style))
    content.append(Spacer(1, 0.3*cm))

    # Imagen captura módulo
    modulo_img = os.path.join(images_dir, 'moduloA.jpeg')
    if os.path.exists(modulo_img):
        try:
            img = Image(modulo_img, width=16*cm, height=9*cm)
            img.hAlign = 'CENTER'
            content.append(img)
            content.append(Spacer(1, 0.3*cm))
            content.append(Paragraph("Figura 2. Vista del módulo de crecimiento de cartera", caption_style))
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    content.append(Paragraph("1.1 Contexto y Problemática", section_style))

    contexto = """
    Estudios recientes indican que aproximadamente el 78% de las personas mayores de 65 años 
    dependen exclusivamente de su pensión de jubilación para cubrir sus gastos básicos. Esta 
    realidad refleja una problemática generalizada: la falta de planificación financiera adecuada 
    durante los años productivos de las personas.
    """
    content.append(Paragraph(contexto, normal_style))
    content.append(Spacer(1, 0.3*cm))

    problematica = """
    La planificación financiera tradicional presenta varios desafíos: complejidad matemática, 
    dificultad para proyectar escenarios futuros, falta de herramientas accesibles y ausencia 
    de educación financiera práctica. Tu Retiro Seguro aborda estos desafíos mediante una 
    plataforma intuitiva que democratiza el acceso a análisis financieros profesionales.
    """
    content.append(Paragraph(problematica, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("1.2 Características Principales del Sistema", section_style))

    caracteristicas = """
    <b>Matemáticas Financieras Avanzadas:</b> El sistema implementa algoritmos basados en 
    conceptos fundamentales del valor del dinero en el tiempo, interés compuesto y proyecciones 
    de flujos de efectivo.<br/><br/>
    
    <b>Interfaz Intuitiva:</b> Diseñada para usuarios sin conocimientos técnicos previos, 
    la plataforma guía al usuario paso a paso en el proceso de planificación financiera.<br/><br/>
    
    <b>Análisis de Escenarios:</b> Permite comparar múltiples escenarios de inversión y jubilación, 
    facilitando la toma de decisiones informadas.<br/><br/>
    
    <b>Gamificación Educativa:</b> Sistema de logros y recompensas que motiva el aprendizaje 
    continuo de conceptos financieros.<br/><br/>
    
    <b>Comunidad de Aprendizaje:</b> Funcionalidades de comparación social que permiten aprender 
    de las estrategias de otros usuarios manteniendo la privacidad de los datos personales.
    """
    content.append(Paragraph(caracteristicas, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("1.3 Beneficios para el Usuario", section_style))

    beneficios = """
    La utilización de Tu Retiro Seguro proporciona múltiples beneficios tangibles para la 
    planificación financiera personal:
    """
    content.append(Paragraph(beneficios, normal_style))
    content.append(Spacer(1, 0.3*cm))

    beneficio_items = [
        "<b>Claridad Financiera:</b> Visualización clara del crecimiento patrimonial proyectado, eliminando la incertidumbre sobre el futuro financiero.",
        "<b>Optimización de Decisiones:</b> Capacidad para comparar diferentes estrategias de ahorro e inversión antes de comprometer recursos.",
        "<b>Eficiencia Temporal:</b> Automatización de cálculos complejos que tradicionalmente requieren horas de análisis manual.",
        "<b>Maximización de Retornos:</b> Identificación de las mejores oportunidades de inversión según el perfil de riesgo individual.",
        "<b>Seguridad en la Planificación:</b> Eliminación de suposiciones mediante proyecciones basadas en modelos matemáticos validados.",
        "<b>Accesibilidad Universal:</b> Disponibilidad 24/7 desde cualquier dispositivo con conexión a internet."
    ]

    for item in beneficio_items:
        content.append(Paragraph(item, list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("1.4 Ventajas Competitivas", section_style))

    ventajas = """
    Tu Retiro Seguro se diferencia de otras soluciones disponibles en el mercado por varios factores:
    """
    content.append(Paragraph(ventajas, normal_style))
    content.append(Spacer(1, 0.3*cm))

    comparacion = """
    <b>Frente a hojas de cálculo tradicionales:</b> Automatiza cálculos complejos y presenta 
    resultados en formatos visuales comprensibles, eliminando la necesidad de conocimientos 
    avanzados en Excel o programación.<br/><br/>
    
    <b>Frente a asesores financieros:</b> Proporciona acceso continuo a análisis profesionales 
    sin costos recurrentes, permitiendo experimentar con múltiples escenarios sin presión comercial.<br/><br/>
    
    <b>Frente a aplicaciones básicas:</b> Implementa modelos matemáticos avanzados que consideran 
    factores como inflación, impuestos y variabilidad de rendimientos, ofreciendo proyecciones más realistas.<br/><br/>
    
    <b>Frente a educación teórica:</b> Combina aprendizaje con aplicación práctica inmediata, 
    permitiendo a los usuarios ver el impacto real de las decisiones financieras en su situación personal.
    """
    content.append(Paragraph(comparacion, normal_style))

    content.append(PageBreak())

    # ==================== CAPÍTULO 2 ====================
    content.append(Paragraph("2. PRIMEROS PASOS", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    primeros_pasos = """
    Este capítulo guía al usuario a través del proceso inicial de utilización de la plataforma, 
    desde el acceso hasta la creación de la primera simulación financiera.
    """
    content.append(Paragraph(primeros_pasos, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("2.1 Acceso a la Plataforma", section_style))

    acceso = """
    Tu Retiro Seguro es una aplicación web que no requiere instalación. Para acceder:
    """
    content.append(Paragraph(acceso, normal_style))
    content.append(Spacer(1, 0.3*cm))

    pasos_acceso = [
        "Abra su navegador web preferido (Chrome, Firefox, Safari o Edge).",
        "Ingrese la URL: https://simulador-finanzas-corporativas-am1t.onrender.com/.",
        "Espere a que cargue la interfaz principal del sistema.",
        "Elija entre crear una cuenta o continuar como usuario anónimo."
    ]

    for i, paso in enumerate(pasos_acceso, 1):
        content.append(Paragraph(f"{i}. {paso}", list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(Spacer(1, 0.5*cm))

    # Imagen formulario
    form_img = os.path.join(images_dir, 'formulario_captura.jpeg')
    if os.path.exists(form_img):
        try:
            img = Image(form_img, width=14*cm, height=8*cm)
            img.hAlign = 'CENTER'
            content.append(img)
            content.append(Spacer(1, 0.3*cm))
            content.append(Paragraph("Figura 3. Formulario de ingreso de datos", caption_style))
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    content.append(Paragraph("2.2 Selección del Módulo de Análisis", section_style))

    modulos_intro = """
    La plataforma ofrece tres módulos principales de análisis, cada uno diseñado para abordar 
    diferentes aspectos de la planificación financiera:
    """
    content.append(Paragraph(modulos_intro, normal_style))
    content.append(Spacer(1, 0.3*cm))

    modulos = """
    <b>Módulo A - Crecimiento de Cartera:</b> Ideal para comenzar la planificación financiera. 
    Permite proyectar cómo crecerá una cartera de inversión considerando aportes periódicos y 
    rendimientos esperados.<br/><br/>
    
    <b>Módulo B - Proyección de Jubilación:</b> Diseñado para planificar la etapa de retiro. 
    Calcula la pensión mensual disponible o la duración de los fondos acumulados durante la jubilación.<br/><br/>
    
    <b>Módulo C - Valoración de Bonos:</b> Herramienta especializada para evaluar instrumentos 
    de renta fija. Determina el valor presente de bonos considerando cupones y valor nominal.
    """
    content.append(Paragraph(modulos, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("2.3 Ingreso de Información", section_style))

    ingreso = """
    Cada módulo presenta un formulario intuitivo donde el usuario ingresa los parámetros relevantes 
    para su análisis. Los campos están diseñados con validaciones que aseguran que la información 
    ingresada sea realista y procesable.<br/><br/>
    
    El sistema proporciona ayudas contextuales y rangos recomendados para cada parámetro, facilitando 
    el ingreso de datos incluso para usuarios sin experiencia previa en finanzas.
    """
    content.append(Paragraph(ingreso, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("2.4 Generación y Análisis de Resultados", section_style))

    resultados = """
    Una vez ingresados los datos, el sistema procesa la información en tiempo real y presenta 
    resultados comprehensivos que incluyen:
    """
    content.append(Paragraph(resultados, normal_style))
    content.append(Spacer(1, 0.3*cm))

    items_resultados = [
        "Resumen ejecutivo con los valores clave de la proyección.",
        "Gráficos interactivos que visualizan la evolución temporal del capital.",
        "Tablas detalladas con proyecciones año por año.",
        "Indicadores financieros relevantes para la toma de decisiones.",
        "Opciones para exportar los resultados en formato PDF."
    ]

    for item in items_resultados:
        content.append(Paragraph(item, list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(PageBreak())

    # ==================== CAPÍTULO 3 ====================
    content.append(Paragraph("3. SISTEMA DE USUARIOS Y PERFILES", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    usuarios_intro = """
    Tu Retiro Seguro implementa un sistema flexible de gestión de usuarios que se adapta a 
    diferentes necesidades y niveles de compromiso con la plataforma.
    """
    content.append(Paragraph(usuarios_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("3.1 Modalidades de Acceso", section_style))

    modalidades = """
    <b>Usuario Anónimo:</b> Permite acceso inmediato a todas las funcionalidades de cálculo 
    sin necesidad de registro. Ideal para usuarios que desean explorar la plataforma o realizar 
    análisis puntuales. Las simulaciones no se guardan permanentemente.<br/><br/>
    
    <b>Usuario Registrado:</b> Requiere creación de cuenta mediante email y contraseña. 
    Proporciona acceso a funcionalidades avanzadas como guardado de simulaciones, historial 
    de análisis, sistema de logros y comparación social. Los datos se mantienen seguros y 
    accesibles desde cualquier dispositivo.
    """
    content.append(Paragraph(modalidades, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("3.2 Perfil de Usuario", section_style))

    perfil = """
    Los usuarios registrados cuentan con un perfil personalizable que incluye:
    """
    content.append(Paragraph(perfil, normal_style))
    content.append(Spacer(1, 0.3*cm))

    perfil_items = [
        "Información personal básica (nombre, edad, ocupación).",
        "Preferencias de visualización y notificaciones.",
        "Historial completo de simulaciones realizadas.",
        "Dashboard personalizado con métricas relevantes.",
        "Configuración de privacidad para la comparación social."
    ]

    for item in perfil_items:
        content.append(Paragraph(item, list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("3.3 Seguridad y Privacidad", section_style))

    seguridad = """
    La plataforma implementa medidas de seguridad robustas para proteger la información de los usuarios:
    """
    content.append(Paragraph(seguridad, normal_style))
    content.append(Spacer(1, 0.3*cm))

    seguridad_items = [
        "Encriptación de contraseñas mediante algoritmos de hashing seguros.",
        "Conexiones HTTPS para todas las comunicaciones con el servidor.",
        "Anonimización de datos en funcionalidades de comparación social.",
        "Cumplimiento con regulaciones de protección de datos personales.",
        "Opciones para exportar o eliminar información personal en cualquier momento."
    ]

    for item in seguridad_items:
        content.append(Paragraph(item, list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(PageBreak())

    # ==================== CAPÍTULO 4 ====================
    content.append(Paragraph("4. MÓDULO A: CRECIMIENTO DE CARTERA DE INVERSIÓN", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    modulo_a_intro = """
    El Módulo A constituye el fundamento de la planificación financiera personal, permitiendo 
    proyectar el crecimiento de una cartera de inversión a lo largo del tiempo considerando 
    aportes periódicos y rendimientos esperados.
    """
    content.append(Paragraph(modulo_a_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    # Imagen resultados módulo A
    results_img = os.path.join(images_dir, 'modulo_a_resultados.jpeg')
    if os.path.exists(results_img):
        try:
            img = Image(results_img, width=14*cm, height=9*cm)
            img.hAlign = 'CENTER'
            content.append(img)
            content.append(Spacer(1, 0.3*cm))
            content.append(Paragraph("Figura 4. Resultados y proyecciones del Módulo A", caption_style))
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    content.append(Paragraph("4.1 Fundamentos Teóricos", section_style))

    fundamentos_a = """
    Este módulo se basa en los principios del valor del dinero en el tiempo y el interés compuesto. 
    La fórmula fundamental utilizada es la del valor futuro de una anualidad:<br/><br/>
    """
    modulo_b_img = os.path.join(images_dir, 'modulo_b_captura.jpeg')
    if os.path.exists(modulo_b_img):
        try:
            img = Image(modulo_b_img, width=14*cm, height=9*cm)
            img.hAlign = 'CENTER'
            content.append(img)
            content.append(Spacer(1, 0.3*cm))
            content.append(Paragraph("Figura 5. Interfaz del Módulo B de jubilación", caption_style))
            content.append(Spacer(1, 0.5*cm))
        except:
            pass
    """
    Donde VF es el valor futuro, VA es el valor actual o capital inicial, i es la tasa de 
    interés por período, n es el número de períodos, y PMT es el pago o aporte periódico.
    """
    content.append(Paragraph(fundamentos_a, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("4.2 Parámetros de Entrada", section_style))

    params_intro = """
    El usuario debe proporcionar los siguientes parámetros para realizar la simulación:
    """
    content.append(Paragraph(params_intro, normal_style))
    content.append(Spacer(1, 0.3*cm))

    parametros_a = [
        "<b>Edad Actual:</b> Edad del usuario al momento de iniciar la inversión. Rango válido: 18 a 100 años.",
        "<b>Capital Inicial:</b> Monto disponible para invertir inmediatamente. Puede ser cero si se planea comenzar solo con aportes periódicos.",
        "<b>Aportes Periódicos:</b> Cantidad que se invertirá regularmente. Este valor debe ser realista según el ingreso disponible del usuario.",
        "<b>Frecuencia de Aportes:</b> Periodicidad con la que se realizarán las inversiones: semanal, mensual o anual.",
        "<b>Edad Meta:</b> Edad objetivo para completar el horizonte de inversión. Debe ser mayor a la edad actual.",
        "<b>Tasa Efectiva Anual (TEA):</b> Rendimiento anual esperado de la inversión. Rango típico: 3% a 15% según el perfil de riesgo."
    ]

    for param in parametros_a:
        content.append(Paragraph(param, list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("4.3 Resultados y Visualizaciones", section_style))

    resultados_a = """
    El sistema genera un conjunto completo de resultados que incluyen:<br/><br/>
    
    <b>Capital Final Acumulado:</b> Monto total disponible al finalizar el período de inversión.<br/><br/>
    
    <b>Total Aportado:</b> Suma de todos los aportes realizados durante el período.<br/><br/>
    
    <b>Intereses Ganados:</b> Diferencia entre el capital final y el total aportado, representando 
    las ganancias generadas por el efecto del interés compuesto.<br/><br/>
    
    <b>Gráfico de Evolución:</b> Visualización temporal del crecimiento de la cartera, mostrando 
    la contribución de los aportes versus los intereses generados.<br/><br/>
    
    <b>Tabla de Proyección:</b> Desglose año por año del saldo, aportes e intereses acumulados.
    """
    content.append(Paragraph(resultados_a, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("4.4 Casos de Uso y Ejemplos", section_style))

    casos_a = """
    <b>Ejemplo 1 - Joven Profesional:</b> Una persona de 25 años con $5,000 de capital inicial, 
    que puede aportar $300 mensuales, esperando jubilarse a los 60 años con un rendimiento 
    conservador del 6% anual, acumulará aproximadamente $400,000.<br/><br/>
    
    <b>Ejemplo 2 - Estrategia Agresiva:</b> Un inversionista de 30 años sin capital inicial, 
    aportando $500 mensuales hasta los 50 años con un rendimiento del 10% anual, puede 
    acumular cerca de $380,000.<br/><br/>
    
    <b>Ejemplo 3 - Planificación a Corto Plazo:</b> Persona de 40 años con $50,000 iniciales, 
    aportando $1,000 mensuales por 10 años al 7% anual, alcanzará aproximadamente $225,000.
    """
    content.append(Paragraph(casos_a, normal_style))

    content.append(PageBreak())

    # ==================== CAPÍTULO 5 ====================
    content.append(Paragraph("5. MÓDULO B: PROYECCIÓN DE JUBILACIÓN", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    modulo_b_intro = """
    El Módulo B permite planificar la etapa de retiro, calculando cuánto dinero mensual se podrá 
    recibir durante la jubilación o cuánto tiempo durarán los fondos acumulados según el estilo 
    de vida deseado.
    """
    content.append(Paragraph(modulo_b_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    # Imagen módulo B
    modulo_b_img = os.path.join(images_dir, 'modulo_b_captura.jpeg')
    if os.path.exists(modulo_b_img):
        try:
            img = Image(modulo_b_img, width=14*cm, height=9*cm)
            img.hAlign = 'CENTER'
            content.append(img)
            content.append(Spacer(1, 0.3*cm))
            content.append(Paragraph("Figura 5. Interfaz del Módulo B de jubilación", caption_style))
            content.append(Spacer(1, 0.5*cm))
        except:
            pass

    content.append(Paragraph("5.1 Modalidades de Retiro", section_style))

    modalidades_retiro = """
    El módulo ofrece dos modalidades principales:<br/><br/>
    
    <b>Pensión Mensual:</b> Calcula cuánto dinero mensual se podrá retirar durante un número 
    específico de años de jubilación, considerando que el capital restante continúa generando 
    rendimientos.<br/><br/>
    
    <b>Retiro Total:</b> Analiza cuánto tiempo durará el capital si se retira una cantidad 
    fija mensual, útil para evaluar la sostenibilidad del estilo de vida planificado.
    """
    content.append(Paragraph(modalidades_retiro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("5.2 Consideraciones Tributarias", section_style))

    tributarias = """
    El sistema incorpora análisis de regímenes tributarios que pueden afectar significativamente 
    los ingresos durante la jubilación:<br/><br/>
    
    <b>Régimen Local:</b> Aplica las tasas impositivas del país de residencia sobre los retiros.<br/><br/>
    
    <b>Régimen Extranjero:</b> Considera tratamientos fiscales alternativos que pueden ser más 
    favorables según acuerdos internacionales.<br/><br/>
    
    La diferencia entre regímenes puede representar variaciones significativas en el ingreso 
    disponible mensual, por lo que es crucial considerar este factor en la planificación.
    """
    content.append(Paragraph(tributarias, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("5.3 Parámetros de Configuración", section_style))

    params_b = [
        "<b>Capital Acumulado:</b> Monto total disponible al inicio de la jubilación, típicamente resultado del Módulo A.",
        "<b>Años de Jubilación:</b> Duración esperada de la etapa de retiro. Se recomienda considerar expectativa de vida más un margen de seguridad.",
        "<b>TEA de Retiro:</b> Rendimiento esperado durante la jubilación, generalmente más conservador (3-5%) que durante acumulación.",
        "<b>Régimen Tributario:</b> Selección del tratamiento fiscal aplicable a los retiros.",
        "<b>Incremento por Inflación:</b> Ajuste opcional para mantener poder adquisitivo constante a lo largo de los años."
    ]

    for param in params_b:
        content.append(Paragraph(param, list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("5.4 Interpretación de Resultados", section_style))

    interpretacion_b = """
    Los resultados del Módulo B deben analizarse considerando varios factores:<br/><br/>
    
    La <b>pensión mensual calculada</b> representa el ingreso bruto antes de impuestos y otros 
    gastos. Es importante comparar este valor con las necesidades reales de gasto mensual.<br/><br/>
    
    La <b>duración del capital</b> debe incluir un margen de seguridad, considerando gastos 
    imprevistos médicos o de emergencia que son más comunes en edad avanzada.<br/><br/>
    
    Se recomienda realizar múltiples simulaciones con diferentes tasas de rendimiento para 
    entender el rango de resultados posibles y planificar escenarios optimistas, realistas y pesimistas.
    """
    content.append(Paragraph(interpretacion_b, normal_style))

    content.append(PageBreak())

    # ==================== CAPÍTULO 6 ====================
    content.append(Paragraph("6. MÓDULO C: VALORACIÓN DE BONOS", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    modulo_c_intro = """
    El Módulo C proporciona herramientas profesionales para evaluar instrumentos de renta fija, 
    específicamente bonos, determinando su valor presente y ayudando en decisiones de inversión.
    """
    content.append(Paragraph(modulo_c_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("6.1 Fundamentos de Valoración de Bonos", section_style))

    fundamentos_bonos = """
    Un bono es un instrumento de deuda donde el emisor se compromete a pagar intereses periódicos 
    (cupones) y devolver el capital (valor nominal) al vencimiento. El valor presente del bono 
    se calcula descontando estos flujos futuros a la tasa de mercado:<br/><br/>
    
    VP = Σ(Cupón/(1+i)^t) + VN/(1+i)^n<br/><br/>
    
    Donde VP es el valor presente, VN es el valor nominal, i es la tasa de descuento (TEA de mercado), 
    t es cada período de pago de cupón, y n es el número total de períodos hasta el vencimiento.
    """
    content.append(Paragraph(fundamentos_bonos, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("6.2 Parámetros del Bono", section_style))

    params_c = [
        "<b>Valor Nominal:</b> Cantidad que el emisor pagará al vencimiento. Típicamente $1,000 o múltiplos.",
        "<b>Tasa Cupón:</b> Porcentaje del valor nominal que se paga periódicamente como interés.",
        "<b>Frecuencia de Pago:</b> Periodicidad de los pagos de cupones: anual, semestral, trimestral.",
        "<b>Plazo al Vencimiento:</b> Años restantes hasta que el bono alcance su fecha de vencimiento.",
        "<b>TEA de Mercado:</b> Tasa de rendimiento requerida por los inversionistas, refleja el riesgo percibido."
    ]

    for param in params_c:
        content.append(Paragraph(param, list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("6.3 Interpretación del Valor Presente", section_style))

    interpretacion_bonos = """
    El valor presente calculado debe compararse con el precio de mercado del bono:<br/><br/>
    
    <b>VP > Precio de Mercado:</b> El bono está subvaluado, representando una oportunidad de compra 
    potencialmente atractiva.<br/><br/>
    
    <b>VP = Precio de Mercado:</b> El bono está correctamente valorado según las condiciones actuales.<br/><br/>
    
    <b>VP < Precio de Mercado:</b> El bono está sobrevalorado, sugiriendo que otras alternativas 
    podrían ofrecer mejor relación riesgo-retorno.<br/><br/>
    
    Es importante considerar que esta valoración asume que el emisor cumplirá con todos los pagos 
    (no hay riesgo de default), por lo que debe evaluarse la calidad crediticia del emisor.
    """
    content.append(Paragraph(interpretacion_bonos, normal_style))

    content.append(PageBreak())

    # ==================== CAPÍTULO 7 ====================
    content.append(Paragraph("7. ANÁLISIS DE ESCENARIOS AVANZADOS", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    escenarios_intro = """
    Una característica distintiva de Tu Retiro Seguro es la capacidad de realizar análisis de 
    sensibilidad y comparación de múltiples escenarios, permitiendo evaluar cómo diferentes 
    suposiciones afectan los resultados finales.
    """
    content.append(Paragraph(escenarios_intro, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("7.1 Análisis de Sensibilidad de Tasas", section_style))

    sensibilidad = """
    El rendimiento de las inversiones rara vez es constante. El análisis de sensibilidad permite 
    visualizar cómo variaciones en la TEA afectan el capital final. Por ejemplo, una diferencia 
    de solo 2% en el rendimiento anual puede significar variaciones de 30-40% en el capital 
    acumulado en horizontes de 20-30 años, demostrando la importancia crítica de la selección 
    de inversiones.
    """
    content.append(Paragraph(sensibilidad, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("7.2 Escenarios de Jubilación Anticipada", section_style))

    anticipada = """
    Muchos usuarios aspiran a jubilarse antes de la edad tradicional. El sistema permite evaluar 
    el impacto de adelantar la jubilación en términos de:<br/><br/>
    
    - Reducción del período de acumulación<br/>
    - Aumento del período de retiro<br/>
    - Necesidad de mayores aportes mensuales<br/>
    - Ajustes en el estilo de vida durante el retiro
    """
    content.append(Paragraph(anticipada, normal_style))
    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("7.3 Consideración de Inflación", section_style))

    inflacion = """
    La inflación erosiona el poder adquisitivo del dinero a lo largo del tiempo. El sistema 
    permite ajustar las proyecciones considerando diferentes tasas de inflación esperadas, 
    mostrando el capital necesario en términos reales para mantener el mismo estilo de vida.
    """
    content.append(Paragraph(inflacion, normal_style))

    content.append(PageBreak())

    # ==================== CAPÍTULOS RESTANTES (Simplificados) ====================
    
    # CAPÍTULO 8
    content.append(Paragraph("8. SISTEMA DE LOGROS Y GAMIFICACIÓN", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    gamification_text = """
    Para mantener la motivación del usuario y fomentar el aprendizaje continuo, la plataforma 
    implementa un sistema de gamificación con logros desbloqueables. Los usuarios ganan insignias 
    al completar hitos como realizar su primera simulación, alcanzar 10 o 50 simulaciones, 
    utilizar funciones avanzadas de comparación, entre otros.<br/><br/>
    
    Este sistema no solo hace más atractiva la experiencia de uso, sino que también guía al 
    usuario a explorar todas las funcionalidades disponibles, maximizando el valor educativo 
    de la plataforma.
    """
    content.append(Paragraph(gamification_text, normal_style))

    content.append(PageBreak())

    # CAPÍTULO 9
    content.append(Paragraph("9. COMPARACIÓN SOCIAL INTELIGENTE", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    social_text = """
    La función de comparación social permite a usuarios registrados ver cómo sus estrategias 
    de ahorro e inversión se comparan con las de otros usuarios en demografías similares (edad, 
    ingreso, horizonte temporal).<br/><br/>
    
    Esta funcionalidad está diseñada con estrictas medidas de privacidad: los datos se presentan 
    de forma agregada y anonimizada, mostrando tendencias y promedios sin revelar información 
    individual identificable.<br/><br/>
    
    Los usuarios pueden obtener insights valiosos sobre si sus tasas de ahorro son competitivas, 
    si sus expectativas de rendimiento son realistas, y descubrir estrategias que han funcionado 
    para otros en situaciones similares.
    """
    content.append(Paragraph(social_text, normal_style))

    content.append(PageBreak())

    # CAPÍTULO 10
    content.append(Paragraph("10. MARKETPLACE DE TEMPLATES", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    marketplace_text = """
    El marketplace ofrece configuraciones predefinidas creadas por expertos financieros y 
    usuarios experimentados. Estos templates cubren escenarios comunes como:<br/><br/>
    
    - <b>Conservador:</b> Perfil de bajo riesgo con énfasis en estabilidad<br/>
    - <b>Moderado:</b> Balance entre crecimiento y seguridad<br/>
    - <b>Agresivo:</b> Maximización de crecimiento con mayor tolerancia al riesgo<br/>
    - <b>FIRE:</b> Estrategias para jubilación anticipada<br/>
    - <b>Familia:</b> Planificación considerando gastos educativos y familiares<br/><br/>
    
    Los usuarios pueden aplicar estos templates directamente o usarlos como punto de partida 
    para personalizaciones, acelerando significativamente el proceso de planificación.
    """
    content.append(Paragraph(marketplace_text, normal_style))

    content.append(PageBreak())

    # CAPÍTULO 11
    content.append(Paragraph("11. REPORTES PROFESIONALES EN PDF", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    reports_text = """
    Cada simulación puede exportarse como un reporte PDF profesional que incluye:<br/><br/>
    
    - Resumen ejecutivo con los resultados principales<br/>
    - Parámetros de entrada utilizados<br/>
    - Gráficos de proyección temporal<br/>
    - Tablas detalladas de flujos año por año<br/>
    - Análisis de sensibilidad cuando aplicable<br/>
    - Metadatos (fecha, versión, usuario)<br/><br/>
    
    Estos reportes son útiles para mantener registro histórico de la planificación, compartir 
    con asesores financieros o familiares, y presentar en contextos profesionales o académicos.
    """
    content.append(Paragraph(reports_text, normal_style))

    content.append(PageBreak())

    # CAPÍTULO 12
    content.append(Paragraph("12. SOPORTE Y SOLUCIÓN DE PROBLEMAS", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    content.append(Paragraph("12.1 Problemas Comunes y Soluciones", section_style))

    problemas = [
        "<b>Error de conexión:</b> Verificar conexión a internet y que el servidor esté accesible.",
        "<b>Resultados inesperados:</b> Revisar que los parámetros ingresados estén en rangos realistas.",
        "<b>No se guardan simulaciones:</b> Confirmar que hay sesión iniciada como usuario registrado.",
        "<b>Gráficos no se visualizan:</b> Asegurar que JavaScript esté habilitado en el navegador.",
        "<b>PDF no se genera:</b> Verificar permisos de descarga y bloqueadores de ventanas emergentes."
    ]

    for problema in problemas:
        content.append(Paragraph(problema, list_style))
        content.append(Spacer(1, 0.2*cm))

    content.append(Spacer(1, 0.5*cm))

    content.append(Paragraph("12.2 Contacto y Asistencia", section_style))

    contacto = """
    Para asistencia adicional o reportar problemas:<br/><br/>
    
    <b>Email:</b> soporte@turetiroseguro.com<br/>
    <b>Web:</b> www.turetiroseguro.com<br/>
    <b>Disponibilidad:</b> Plataforma online 24/7
    """
    content.append(Paragraph(contacto, normal_style))

    content.append(PageBreak())

    # CAPÍTULO 13
    content.append(Paragraph("13. GLOSARIO DE TÉRMINOS FINANCIEROS", chapter_style))
    content.append(Spacer(1, 0.3*cm))

    glosario_items = [
        "<b>Anualidad:</b> Serie de pagos periódicos iguales realizados a intervalos regulares.",
        "<b>Capitalización:</b> Proceso de reinvertir ganancias para generar rendimientos adicionales.",
        "<b>Duration:</b> Medida de la sensibilidad del precio de un bono a cambios en tasas de interés.",
        "<b>Horizonte Temporal:</b> Período de tiempo considerado para una inversión.",
        "<b>Interés Compuesto:</b> Interés calculado sobre el capital inicial más los intereses acumulados.",
        "<b>Liquidez:</b> Facilidad con la que un activo puede convertirse en efectivo.",
        "<b>Riesgo de Crédito:</b> Probabilidad de que un emisor no cumpla con sus obligaciones de pago.",
        "<b>Tasa Cupón:</b> Tasa de interés anual que paga un bono sobre su valor nominal.",
        "<b>TEA (Tasa Efectiva Anual):</b> Tasa de interés anual considerando el efecto de la capitalización.",
        "<b>Valor Nominal:</b> Valor facial de un instrumento financiero pagadero al vencimiento.",
        "<b>Valor Presente:</b> Valor actual de flujos de efectivo futuros descontados a una tasa específica.",
        "<b>Volatilidad:</b> Grado de variación en los rendimientos de una inversión."
    ]

    for item in glosario_items:
        content.append(Paragraph(item, list_style))
        content.append(Spacer(1, 0.3*cm))

    content.append(PageBreak())

    # ==================== CONCLUSIÓN ====================
    content.append(Spacer(1, 2*cm))
    
    conclusion_title = Paragraph("CONCLUSIÓN", chapter_style)
    content.append(conclusion_title)
    content.append(Spacer(1, 0.5*cm))

    conclusion_text = """
    Tu Retiro Seguro representa una herramienta integral para la planificación financiera personal, 
    democratizando el acceso a análisis que tradicionalmente requerían asesores financieros costosos 
    o conocimientos técnicos especializados.<br/><br/>
    
    La combinación de rigor matemático, interfaz intuitiva y funcionalidades educativas hace de 
    esta plataforma un recurso invaluable para cualquier persona comprometida con asegurar su 
    futuro financiero.<br/><br/>
    
    Se recomienda a los usuarios realizar simulaciones periódicas, ajustando parámetros conforme 
    cambian sus circunstancias personales y las condiciones del mercado. La planificación financiera 
    es un proceso continuo, no un evento único, y esta herramienta está diseñada para acompañarle 
    en cada etapa de ese viaje.<br/><br/>
    
    El equipo de desarrollo continúa trabajando en mejoras y nuevas funcionalidades. Sus comentarios 
    y sugerencias son bienvenidos y contribuyen a hacer de Tu Retiro Seguro una herramienta cada 
    vez más útil para la comunidad.
    """
    content.append(Paragraph(conclusion_text, normal_style))
    content.append(Spacer(1, 2*cm))

    # Footer final
    footer_final = """
    <b>Tu Retiro Seguro</b><br/>
    Simulador Financiero de Jubilación<br/>
    Manual de Usuario - Versión 2.0<br/>
    Noviembre 2025<br/><br/>
    Desarrollado por: Unidad II - Finanzas Corporativas<br/>
    © 2025 Todos los derechos reservados
    """
    content.append(Paragraph(footer_final, ParagraphStyle('footer', parent=normal_style, 
                                                          alignment=TA_CENTER, fontSize=9, 
                                                          textColor=COLOR_GRIS)))

    # Generar PDF
    try:
        doc.build(content, canvasmaker=NumberedCanvas)
        print(f"✅ Manual de usuario creado exitosamente")
        print(f"📄 Ubicación: {filename}")
        print(f"\n📁 Carpeta de imágenes: {images_dir}")
        print("\n📸 Imágenes opcionales que puedes agregar:")
        print("   • logo_universidad.png (4x4 cm)")
        print("   • dashboard_principal.png (12x8 cm)")
        print("   • modulo_a_captura.png (14x8 cm)")
        print("   • modulo_a_resultados.png (14x9 cm)")
        print("   • modulo_b_captura.png (14x9 cm)")
        print("   • modulo_c_captura.png (14x9 cm)")
        print("   • formulario_captura.png (13x9 cm)")
        print("   • logros_captura.png (14x8 cm)")
        return filename
    except Exception as e:
        print(f"❌ Error al generar PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    crear_manual_usuario()