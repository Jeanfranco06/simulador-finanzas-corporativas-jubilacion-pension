"""
Módulo de exportación a PDF
Genera reportes en PDF con los resultados de las simulaciones
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import pandas as pd
from datetime import datetime
from typing import Dict, Optional
import io


def crear_estilos_personalizados():
    """
    Crea estilos personalizados para el documento PDF
    
    Returns:
        Dict con estilos personalizados
    """
    estilos = getSampleStyleSheet()
    
    # Estilo para título principal
    estilo_titulo = ParagraphStyle(
        'TituloPersonalizado',
        parent=estilos['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulos
    estilo_subtitulo = ParagraphStyle(
        'SubtituloPersonalizado',
        parent=estilos['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2e5c9a'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para texto normal
    estilo_normal = ParagraphStyle(
        'NormalPersonalizado',
        parent=estilos['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    # Estilo para resumen destacado
    estilo_resumen = ParagraphStyle(
        'ResumenPersonalizado',
        parent=estilos['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        spaceBefore=6,
        leftIndent=20,
        fontName='Helvetica-Bold'
    )
    
    return {
        'titulo': estilo_titulo,
        'subtitulo': estilo_subtitulo,
        'normal': estilo_normal,
        'resumen': estilo_resumen
    }


def crear_tabla_estilizada(df: pd.DataFrame, columnas_a_mostrar: Optional[list] = None) -> Table:
    """
    Crea una tabla estilizada para el PDF
    
    Args:
        df: DataFrame con los datos
        columnas_a_mostrar: Lista de columnas a incluir (None = todas)
    
    Returns:
        Objeto Table de ReportLab
    """
    if columnas_a_mostrar:
        df = df[columnas_a_mostrar]
    
    # Convertir DataFrame a lista de listas
    datos = [df.columns.tolist()] + df.values.tolist()
    
    # Crear tabla
    tabla = Table(datos)
    
    # Estilo de la tabla
    estilo = TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Contenido
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ])
    
    tabla.setStyle(estilo)
    
    return tabla


def generar_pdf_cartera(
    df_cartera: pd.DataFrame,
    resumen: Dict,
    ruta_grafica: Optional[str] = None
) -> bytes:
    """
    Genera un PDF con los resultados de la simulación de cartera
    
    Args:
        df_cartera: DataFrame con el detalle de la cartera
        resumen: Diccionario con el resumen de resultados
        ruta_grafica: Ruta opcional de la gráfica a incluir
    
    Returns:
        Bytes del PDF generado
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    estilos = crear_estilos_personalizados()
    
    # Título
    titulo = Paragraph("Reporte de Simulación de Cartera", estilos['titulo'])
    story.append(titulo)
    story.append(Spacer(1, 0.2*inch))
    
    # Fecha
    fecha = Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilos['normal'])
    story.append(fecha)
    story.append(Spacer(1, 0.3*inch))
    
    # Resumen Ejecutivo
    story.append(Paragraph("📊 Resumen Ejecutivo", estilos['subtitulo']))
    
    for clave, valor in resumen.items():
        if isinstance(valor, (int, float)):
            texto = f"<b>{clave}:</b> ${valor:,.2f} USD"
        else:
            texto = f"<b>{clave}:</b> {valor}"
        story.append(Paragraph(texto, estilos['resumen']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Gráfica (si existe)
    if ruta_grafica:
        try:
            story.append(Paragraph("📈 Evolución de la Cartera", estilos['subtitulo']))
            img = RLImage(ruta_grafica, width=6*inch, height=3.5*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
        except:
            pass
    
    # Tabla detallada (primeros y últimos 10 periodos)
    story.append(Paragraph("📋 Detalle de Periodos", estilos['subtitulo']))
    
    if len(df_cartera) > 20:
        df_mostrar = pd.concat([df_cartera.head(10), df_cartera.tail(10)])
        nota = Paragraph("(Se muestran los primeros y últimos 10 periodos)", estilos['normal'])
        story.append(nota)
    else:
        df_mostrar = df_cartera
    
    tabla = crear_tabla_estilizada(df_mostrar)
    story.append(tabla)
    
    # Construir PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer.getvalue()


def generar_pdf_bono(
    df_flujos: pd.DataFrame,
    resumen_bono: Dict
) -> bytes:
    """
    Genera un PDF con los resultados de la valoración de bonos
    
    Args:
        df_flujos: DataFrame con los flujos del bono
        resumen_bono: Diccionario con el resumen del bono
    
    Returns:
        Bytes del PDF generado
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    estilos = crear_estilos_personalizados()
    
    # Título
    titulo = Paragraph("Reporte de Valoración de Bonos", estilos['titulo'])
    story.append(titulo)
    story.append(Spacer(1, 0.2*inch))
    
    # Fecha
    fecha = Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilos['normal'])
    story.append(fecha)
    story.append(Spacer(1, 0.3*inch))
    
    # Resumen
    story.append(Paragraph("💰 Resumen de Valoración", estilos['subtitulo']))
    
    for clave, valor in resumen_bono.items():
        if isinstance(valor, (int, float)):
            texto = f"<b>{clave}:</b> ${valor:,.2f} USD"
        else:
            texto = f"<b>{clave}:</b> {valor}"
        story.append(Paragraph(texto, estilos['resumen']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Tabla de flujos
    story.append(Paragraph("📋 Flujos del Bono", estilos['subtitulo']))
    
    tabla = crear_tabla_estilizada(df_flujos)
    story.append(tabla)
    
    # Construir PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer.getvalue()


def generar_pdf_completo(
    df_cartera: pd.DataFrame,
    resumen_cartera: Dict,
    resumen_jubilacion: Dict,
    df_bono: Optional[pd.DataFrame] = None,
    resumen_bono: Optional[Dict] = None,
    ruta_grafica: Optional[str] = None
) -> bytes:
    """
    Genera un PDF completo con todos los módulos
    
    Args:
        df_cartera: DataFrame con el detalle de la cartera
        resumen_cartera: Resumen de la cartera
        resumen_jubilacion: Resumen de la jubilación
        df_bono: DataFrame opcional con flujos del bono
        resumen_bono: Resumen opcional del bono
        ruta_grafica: Ruta opcional de la gráfica
    
    Returns:
        Bytes del PDF generado
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    estilos = crear_estilos_personalizados()
    
    # Portada
    titulo = Paragraph("Reporte Financiero Completo", estilos['titulo'])
    story.append(titulo)
    story.append(Spacer(1, 0.1*inch))
    
    subtitulo = Paragraph("Simulador de Jubilación y Valoración de Bonos", estilos['subtitulo'])
    story.append(subtitulo)
    story.append(Spacer(1, 0.2*inch))
    
    fecha = Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilos['normal'])
    story.append(fecha)
    story.append(Spacer(1, 0.5*inch))
    
    # Módulo A: Cartera
    story.append(Paragraph("MÓDULO A: CRECIMIENTO DE CARTERA", estilos['subtitulo']))
    
    for clave, valor in resumen_cartera.items():
        if isinstance(valor, (int, float)):
            texto = f"<b>{clave}:</b> ${valor:,.2f} USD"
        else:
            texto = f"<b>{clave}:</b> {valor}"
        story.append(Paragraph(texto, estilos['resumen']))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Gráfica
    if ruta_grafica:
        try:
            img = RLImage(ruta_grafica, width=6*inch, height=3*inch)
            story.append(img)
            story.append(Spacer(1, 0.2*inch))
        except:
            pass
    
    # Módulo B: Jubilación
    story.append(PageBreak())
    story.append(Paragraph("MÓDULO B: PROYECCIÓN DE JUBILACIÓN", estilos['subtitulo']))
    
    for clave, valor in resumen_jubilacion.items():
        if isinstance(valor, (int, float)):
            texto = f"<b>{clave}:</b> ${valor:,.2f} USD"
        else:
            texto = f"<b>{clave}:</b> {valor}"
        story.append(Paragraph(texto, estilos['resumen']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # Tabla de cartera (resumen)
    if len(df_cartera) > 20:
        df_mostrar = pd.concat([df_cartera.head(10), df_cartera.tail(10)])
    else:
        df_mostrar = df_cartera
    
    tabla = crear_tabla_estilizada(df_mostrar)
    story.append(tabla)
    
    # Módulo C: Bonos (si existe)
    if df_bono is not None and resumen_bono is not None:
        story.append(PageBreak())
        story.append(Paragraph("MÓDULO C: VALORACIÓN DE BONOS", estilos['subtitulo']))
        
        for clave, valor in resumen_bono.items():
            if isinstance(valor, (int, float)):
                texto = f"<b>{clave}:</b> ${valor:,.2f} USD"
            else:
                texto = f"<b>{clave}:</b> {valor}"
            story.append(Paragraph(texto, estilos['resumen']))
        
        story.append(Spacer(1, 0.3*inch))
        
        tabla_bono = crear_tabla_estilizada(df_bono)
        story.append(tabla_bono)
    
    # Construir PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer.getvalue()
