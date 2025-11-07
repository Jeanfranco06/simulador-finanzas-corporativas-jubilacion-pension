"""
PDF generation utilities for the Financial Simulator
"""
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
from reportlab.platypus.flowables import KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import pandas as pd
from datetime import datetime

class PDFGenerator:
    """Class for generating professional PDF reports"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_colors()
        self._setup_styles()

    def _setup_colors(self):
        """Setup color scheme for the PDF"""
        self.primary_color = HexColor('#1f2937')  # Dark gray
        self.secondary_color = HexColor('#3b82f6')  # Blue
        self.accent_color = HexColor('#10b981')  # Green
        self.warning_color = HexColor('#f59e0b')  # Amber
        self.light_bg = HexColor('#f8fafc')  # Light gray background
        self.table_header_bg = HexColor('#e2e8f0')  # Light blue header
        self.positive_color = HexColor('#059669')  # Green for positive values
        self.negative_color = HexColor('#dc2626')  # Red for negative values

    def _setup_styles(self):
        """Setup custom styles for the PDF"""
        # Main title
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            fontName='Helvetica-Bold',
            textColor=self.primary_color,
            spaceAfter=20,
            alignment=1,  # Center
            spaceBefore=20
        )

        # Subtitle
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            fontName='Helvetica-Bold',
            textColor=self.secondary_color,
            spaceAfter=15,
            spaceBefore=10
        )

        # Section headers
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            fontName='Helvetica-Bold',
            textColor=self.primary_color,
            spaceAfter=10,
            spaceBefore=15
        )

        # Normal text
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica',
            spaceAfter=8,
            leading=14
        )

        # Small text for details
        self.small_style = ParagraphStyle(
            'CustomSmall',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica',
            textColor=colors.gray,
            spaceAfter=6
        )

        # Footer style
        self.footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica',
            textColor=colors.gray,
            alignment=1
        )

    def generate_portfolio_report(self, df, resumen, grafica_path=None):
        """Generate professional PDF report for portfolio simulation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        elements = []

        # Header with branding
        header_data = [
            [Paragraph("SIMULADOR FINANCIERO", ParagraphStyle('HeaderMain',
                fontSize=18, fontName='Helvetica-Bold', textColor=self.primary_color, alignment=0)),
             Paragraph("Reporte Profesional", ParagraphStyle('HeaderSub',
                fontSize=12, fontName='Helvetica', textColor=self.secondary_color, alignment=2))]
        ]
        header_table = Table(header_data, colWidths=[10*cm, 6*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 10))  # Add space before the line
        elements.append(HRFlowable(width="100%", thickness=2, color=self.secondary_color, spaceAfter=20))

        # Main Title
        elements.append(Paragraph("Simulación de Crecimiento de Cartera", self.title_style))
        elements.append(Paragraph("Análisis detallado de proyección financiera", self.small_style))
        elements.append(Spacer(1, 15))

        # Generation info
        info_data = [
            ["Fecha de generación:", datetime.now().strftime('%d/%m/%Y %H:%M')],
            ["Tipo de análisis:", "Proyección de inversión con interés compuesto"],
            ["Moneda:", "USD (Dólares Americanos)"]
        ]
        info_table = Table(info_data, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # Executive Summary Section
        elements.append(Paragraph("📊 RESUMEN EJECUTIVO", self.section_style))
        elements.append(Paragraph("Principales indicadores financieros del análisis", self.normal_style))

        # Key metrics in a highlighted box
        key_metrics_data = [
            ["Métrica", "Valor", "Interpretación"],
            ["Capital Final", f"${resumen['capital_final']:,.2f}",
             "Monto total acumulado al final del período"],
            ["Aportes Totales", f"${resumen['aportes_totales']:,.2f}",
             "Suma de todas las inversiones realizadas"],
            ["Ganancia Bruta", f"${resumen['ganancia_bruta']:,.2f}",
             "Retorno generado por el interés compuesto"],
            ["Rentabilidad Total", f"{resumen['rentabilidad']:.2f}%",
             "Porcentaje de retorno sobre la inversión"]
        ]

        key_metrics_table = Table(key_metrics_data, colWidths=[3.5*cm, 3.5*cm, 9*cm])
        key_metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.secondary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(key_metrics_table)
        elements.append(Spacer(1, 15))

        # Investment Parameters
        elements.append(Paragraph("🔧 PARÁMETROS DE INVERSIÓN", self.section_style))
        params_data = [
            ["Edad Actual", f"{resumen.get('edad_actual', 'N/A')} años"],
            ["Edad de Retiro", f"{resumen['edad_retiro']} años"],
            ["Período de Inversión", f"{resumen['años']} años"],
            ["Frecuencia de Aportes", resumen['frecuencia']],
            ["Monto Inicial", f"${resumen.get('monto_inicial', 0):,.2f}"],
            ["Aporte Periódico", f"${resumen.get('aporte_periodico', 0):,.2f}"],
            ["TEA", f"{resumen.get('tea', 0):.2f}%"]
        ]

        params_table = Table(params_data, colWidths=[5*cm, 11*cm])
        params_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(params_table)
        elements.append(Spacer(1, 20))

        # Chart Section
        if grafica_path:
            elements.append(Paragraph("📈 EVOLUCIÓN DE LA CARTERA", self.section_style))
            elements.append(Paragraph("Visualización gráfica del crecimiento del capital a lo largo del tiempo", self.normal_style))
            try:
                img = Image(grafica_path, 14*cm, 8*cm)
                img.hAlign = 'CENTER'
                elements.append(Spacer(1, 10))
                elements.append(img)
                elements.append(Spacer(1, 15))
            except Exception as e:
                elements.append(Paragraph(f"Nota: No se pudo cargar la gráfica ({str(e)})", self.small_style))
                elements.append(Spacer(1, 10))

        # Key Insights
        elements.append(Paragraph("💡 ANÁLISIS Y CONCLUSIONES", self.section_style))

        # Calculate some insights
        total_periods = len(df)
        avg_monthly_contribution = resumen.get('aporte_periodico', 0)
        total_contributions = resumen['aportes_totales']
        total_growth = resumen['ganancia_bruta']

        insights = [
            f"• El análisis cubre un período de {resumen['años']} años ({total_periods} períodos de aportes)",
            f"• Se proyecta un crecimiento total de ${total_growth:,.2f} generado por interés compuesto",
            f"• La rentabilidad total del {resumen['rentabilidad']:.2f}% representa el retorno sobre la inversión",
            f"• Los aportes periódicos representan el {((total_contributions - resumen.get('monto_inicial', 0)) / total_contributions * 100):.1f}% del capital total",
            f"• El interés compuesto genera el {(total_growth / total_contributions * 100):.1f}% del capital final"
        ]

        for insight in insights:
            elements.append(Paragraph(insight, self.normal_style))

        elements.append(Spacer(1, 20))

        # Detailed Results Table
        elements.append(Paragraph("📋 DETALLE PERIÓDICO COMPLETO", self.section_style))
        elements.append(Paragraph(f"Evolución mensual/anual del capital - Total de {len(df)} períodos", self.normal_style))

        # Show all periods in the table
        table_data = [['Periodo', 'Saldo Inicial', 'Aportes', 'Interés', 'Saldo Final', 'Aportes Acum.']]
        for _, row in df.iterrows():
            table_data.append([
                str(int(row['Periodo'])),
                f"${row['Saldo Inicial']:,.2f}",
                f"${row['Aportes']:,.2f}",
                f"${row['Interés']:,.2f}",
                f"${row['Saldo Final']:,.2f}",
                f"${row['Aportes Acumulados']:,.2f}"
            ])

        # Create table - use smaller font for many rows
        font_size = 7 if len(df) > 50 else 8  # Smaller font for very long tables
        col_widths = [1.2*cm, 2.2*cm, 1.8*cm, 1.8*cm, 2.2*cm, 2.8*cm] if len(df) > 50 else [1.5*cm, 2.5*cm, 2*cm, 2*cm, 2.5*cm, 3*cm]

        full_table = Table(table_data, colWidths=col_widths, repeatRows=1)  # repeatRows=1 to repeat header on new pages
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.table_header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.primary_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ('FONTSIZE', (0, 1), (-1, -1), font_size),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])
        full_table.setStyle(table_style)
        elements.append(full_table)

        # Footer
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=10))
        elements.append(Paragraph("Reporte generado por Simulador Financiero - Todos los cálculos son proyecciones basadas en los parámetros proporcionados", self.footer_style))
        elements.append(Paragraph(f"Página 1 - Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", self.footer_style))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def _get_table_style(self):
        """Get consistent table styling"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.table_header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.primary_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ])

    def generate_bond_report(self, df, resumen):
        """Generate professional PDF report for bond valuation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        elements = []

        # Header with branding
        header_data = [
            [Paragraph("SIMULADOR FINANCIERO", ParagraphStyle('HeaderMain',
                fontSize=18, fontName='Helvetica-Bold', textColor=self.primary_color, alignment=0)),
             Paragraph("Reporte Profesional", ParagraphStyle('HeaderSub',
                fontSize=12, fontName='Helvetica', textColor=self.secondary_color, alignment=2))]
        ]
        header_table = Table(header_data, colWidths=[10*cm, 6*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=2, color=self.secondary_color, spaceAfter=20))

        # Main Title
        elements.append(Paragraph("Valoración de Bonos", self.title_style))
        elements.append(Paragraph("Análisis detallado de valoración de instrumento de deuda", self.small_style))
        elements.append(Spacer(1, 15))

        # Generation info
        info_data = [
            ["Fecha de generación:", datetime.now().strftime('%d/%m/%Y %H:%M')],
            ["Tipo de análisis:", "Valoración de bono con descuento de flujos"],
            ["Moneda:", "USD (Dólares Americanos)"]
        ]
        info_table = Table(info_data, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # Executive Summary Section
        elements.append(Paragraph("📊 RESUMEN EJECUTIVO", self.section_style))
        elements.append(Paragraph("Principales indicadores de la valoración del bono", self.normal_style))

        # Key metrics in a highlighted box
        estado_color = self.positive_color if resumen['estado'] == 'Prima' else \
                      self.negative_color if resumen['estado'] == 'Descuento' else \
                      self.warning_color

        key_metrics_data = [
            ["Métrica", "Valor", "Interpretación"],
            ["Valor Presente Total", f"${resumen['valor_presente_total']:,.2f}",
             "Precio justo del bono en el mercado actual"],
            ["Valor Nominal", f"${resumen['valor_nominal']:,.2f}",
             "Valor facial del bono al vencimiento"],
            ["Prima/Descuento", f"${resumen['diferencia']:,.2f}",
             "Diferencia entre valor presente y nominal"],
            ["Estado del Bono", resumen['estado'],
             "Cotización relativa al valor nominal"],
            ["Tasa Cupón", f"{resumen['tasa_cupon']:.2f}%",
             "Tasa de interés nominal del bono"],
            ["TEA Requerida", f"{resumen.get('tea_retorno', 0):.2f}%",
             "Tasa de descuento utilizada en la valoración"]
        ]

        key_metrics_table = Table(key_metrics_data, colWidths=[3.5*cm, 3.5*cm, 9*cm])
        key_metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.secondary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            # Color the status row
            ('TEXTCOLOR', (1, 3), (1, 3), estado_color),
            ('FONTNAME', (1, 3), (1, 3), 'Helvetica-Bold'),
        ]))
        elements.append(key_metrics_table)
        elements.append(Spacer(1, 15))

        # Bond Characteristics
        elements.append(Paragraph("🔧 CARACTERÍSTICAS DEL BONO", self.section_style))
        params_data = [
            ["Valor Nominal", f"${resumen['valor_nominal']:,.2f}"],
            ["Tasa Cupón Anual", f"{resumen['tasa_cupon']:.2f}%"],
            ["Frecuencia de Pago", resumen.get('frecuencia_pago', 'Anual').title()],
            ["Plazo al Vencimiento", f"{resumen.get('años_bono', 0)} años"],
            ["TEA de Mercado", f"{resumen.get('tea_retorno', 0):.2f}%"]
        ]

        params_table = Table(params_data, colWidths=[5*cm, 11*cm])
        params_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(params_table)
        elements.append(Spacer(1, 20))

        # Bond Analysis
        elements.append(Paragraph("💡 ANÁLISIS DE VALORACIÓN", self.section_style))

        # Determine analysis based on bond status
        if resumen['estado'] == 'Prima':
            analysis_points = [
                f"• El bono cotiza con <b>PRIMA</b> de ${resumen['diferencia']:,.2f} sobre su valor nominal",
                f"• La tasa cupón ({resumen['tasa_cupon']:.2f}%) es <b>superior</b> a la TEA requerida ({resumen.get('tea_retorno', 0):.2f}%)",
                f"• Los inversionistas están dispuestos a pagar más por los cupones atractivos",
                f"• Valor presente total: ${resumen['valor_presente_total']:,.2f}",
                f"• El bono ofrece mayor rentabilidad que las alternativas de mercado"
            ]
        elif resumen['estado'] == 'Descuento':
            analysis_points = [
                f"• El bono cotiza con <b>DESCUENTO</b> de ${abs(resumen['diferencia']):,.2f} bajo su valor nominal",
                f"• La tasa cupón ({resumen['tasa_cupon']:.2f}%) es <b>inferior</b> a la TEA requerida ({resumen.get('tea_retorno', 0):.2f}%)",
                f"• El descuento compensa la tasa de cupón menos atractiva",
                f"• Valor presente total: ${resumen['valor_presente_total']:,.2f}",
                f"• Oportunidad de compra a precio reducido"
            ]
        else:
            analysis_points = [
                f"• El bono cotiza a la <b>PAR</b> (valor presente = valor nominal)",
                f"• La tasa cupón ({resumen['tasa_cupon']:.2f}%) es <b>igual</b> a la TEA requerida ({resumen.get('tea_retorno', 0):.2f}%)",
                f"• Valoración equilibrada entre tasa de cupón y requerimientos de mercado",
                f"• Valor presente total: ${resumen['valor_presente_total']:,.2f}",
                f"• Precio justo de mercado"
            ]

        for point in analysis_points:
            elements.append(Paragraph(point, self.normal_style))

        elements.append(Spacer(1, 20))

        # Cash Flows Table
        elements.append(Paragraph("📋 FLUJOS DE EFECTIVO DETALLADOS", self.section_style))
        elements.append(Paragraph(f"Desglose completo de pagos e intereses descontados - Total de {len(df)} períodos", self.normal_style))

        # Prepare table data
        table_data = [['Periodo', 'Flujo de Caja (USD)', 'Valor Presente (USD)']]
        for _, row in df.iterrows():
            table_data.append([
                str(int(row['Periodo'])),
                f"${row['Flujo (USD)']:,.2f}",
                f"${row['Valor Presente (USD)']:,.2f}"
            ])

        # Create table with appropriate sizing
        font_size = 7 if len(df) > 50 else 8
        col_widths = [2*cm, 3.5*cm, 3.5*cm] if len(df) > 50 else [2.5*cm, 4*cm, 4*cm]

        flows_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.table_header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.primary_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ('FONTSIZE', (0, 1), (-1, -1), font_size),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])
        flows_table.setStyle(table_style)
        elements.append(flows_table)

        # Footer
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=10))
        elements.append(Paragraph("Reporte generado por Simulador Financiero - Todos los cálculos son valoraciones basadas en los parámetros proporcionados", self.footer_style))
        elements.append(Paragraph(f"Página 1 - Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", self.footer_style))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_retirement_report(self, resumen):
        """Generate professional PDF report for retirement projection"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        elements = []

        # Header with branding
        header_data = [
            [Paragraph("SIMULADOR FINANCIERO", ParagraphStyle('HeaderMain',
                fontSize=18, fontName='Helvetica-Bold', textColor=self.primary_color, alignment=0)),
             Paragraph("Reporte Profesional", ParagraphStyle('HeaderSub',
                fontSize=12, fontName='Helvetica', textColor=self.secondary_color, alignment=2))]
        ]
        header_table = Table(header_data, colWidths=[10*cm, 6*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=2, color=self.secondary_color, spaceAfter=20))

        # Main Title
        elements.append(Paragraph("Proyección de Jubilación", self.title_style))
        elements.append(Paragraph("Análisis detallado de planificación financiera para el retiro", self.small_style))
        elements.append(Spacer(1, 15))

        # Generation info
        info_data = [
            ["Fecha de generación:", datetime.now().strftime('%d/%m/%Y %H:%M')],
            ["Tipo de análisis:", "Proyección de pensión con impuestos"],
            ["Moneda:", "USD (Dólares Americanos)"]
        ]
        info_table = Table(info_data, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # Executive Summary Section
        elements.append(Paragraph("📊 RESUMEN EJECUTIVO", self.section_style))
        elements.append(Paragraph("Principales indicadores de la proyección de jubilación", self.normal_style))

        # Key metrics in a highlighted box
        tipo_retiro = "Pensión Mensual" if resumen.get('tipo_retiro') == 'pension' else "Retiro Total"

        if resumen.get('tipo_retiro') == 'pension':
            key_metrics_data = [
                ["Métrica", "Valor", "Interpretación"],
                ["Capital Inicial", f"${resumen.get('capital_inicial', 0):,.2f}",
                 "Monto disponible para generar pensión"],
                ["Pensión Mensual Neta", f"${resumen.get('pension_mensual_neta', 0):,.2f}",
                 "Ingreso mensual después de impuestos"],
                ["Pensión Anual Neta", f"${resumen.get('pension_anual_neta', 0):,.2f}",
                 "Ingreso anual después de impuestos"],
                ["Años de Retiro", f"{resumen.get('años_retiro', 0)} años",
                 "Duración estimada de la pensión"],
                ["TEA de Retiro", f"{resumen.get('tea_retiro', 0):.2f}%",
                 "Tasa efectiva anual utilizada"],
                ["Tipo de Impuesto", resumen.get('tipo_impuesto', '').title(),
                 "Régimen tributario aplicado"]
            ]
        else:
            key_metrics_data = [
                ["Métrica", "Valor", "Interpretación"],
                ["Capital Inicial", f"${resumen.get('capital_inicial', 0):,.2f}",
                 "Monto disponible para retiro"],
                ["Retiro Total Neto", f"${resumen.get('pension_mensual_neta', 0):,.2f}",
                 "Monto total después de impuestos"],
                ["Impuesto Total", f"${resumen.get('impuesto_mensual', 0):,.2f}",
                 "Total de impuestos retenidos"],
                ["TEA de Retiro", f"{resumen.get('tea_retiro', 0):.2f}%",
                 "Tasa efectiva anual utilizada"],
                ["Tipo de Impuesto", resumen.get('tipo_impuesto', '').title(),
                 "Régimen tributario aplicado"],
                ["Tipo de Retiro", "Retiro Total",
                 "Modalidad de retiro seleccionada"]
            ]

        key_metrics_table = Table(key_metrics_data, colWidths=[3.5*cm, 3.5*cm, 9*cm])
        key_metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.secondary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(key_metrics_table)
        elements.append(Spacer(1, 15))

        # Retirement Parameters
        elements.append(Paragraph("🔧 PARÁMETROS DE JUBILACIÓN", self.section_style))
        params_data = [
            ["Tipo de Retiro", tipo_retiro],
            ["Tipo de Impuesto", resumen.get('tipo_impuesto', '').title()],
            ["Capital Inicial", f"${resumen.get('capital_inicial', 0):,.2f}"]
        ]

        if resumen.get('tipo_retiro') == 'pension':
            params_data.extend([
                ["Años de Retiro", f"{resumen.get('años_retiro', 0)} años"],
                ["TEA de Retiro", f"{resumen.get('tea_retiro', 0):.2f}%"],
                ["Usar TEA de Cartera", "Sí" if resumen.get('usar_misma_tea') else "No"]
            ])
        else:
            params_data.extend([
                ["TEA de Retiro", f"{resumen.get('tea_retiro', 0):.2f}%"],
                ["Usar TEA de Cartera", "Sí" if resumen.get('usar_misma_tea') else "No"]
            ])

        params_table = Table(params_data, colWidths=[5*cm, 11*cm])
        params_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(params_table)
        elements.append(Spacer(1, 20))

        # Retirement Analysis
        elements.append(Paragraph("💡 ANÁLISIS DE JUBILACIÓN", self.section_style))

        # Calculate some insights
        capital_inicial = resumen.get('capital_inicial', 0)
        pension_neta = resumen.get('pension_mensual_neta', 0)
        impuesto_total = resumen.get('impuesto_mensual', 0)

        if resumen.get('tipo_retiro') == 'pension':
            años_retiro = resumen.get('años_retiro', 0)
            pension_anual_neta = resumen.get('pension_anual_neta', 0)
            total_pensiones = pension_anual_neta * años_retiro

            analysis_points = [
                f"• Se proyecta una <b>pensión mensual neta</b> de ${pension_neta:,.2f}",
                f"• La pensión anual neta sería de ${pension_anual_neta:,.2f}",
                f"• Total de pensiones proyectadas: ${total_pensiones:,.2f} en {años_retiro} años",
                f"• Impuestos retenidos mensualmente: ${resumen.get('impuesto_mensual', 0):,.2f}",
                f"• El capital inicial de ${capital_inicial:,.2f} generará ingresos estables",
                f"• Planificación financiera para {años_retiro} años de retiro confortable"
            ]
        else:
            analysis_points = [
                f"• Se proyecta un <b>retiro total neto</b> de ${pension_neta:,.2f}",
                f"• Impuestos retenidos en el retiro: ${impuesto_total:,.2f}",
                f"• El capital inicial de ${capital_inicial:,.2f} estará disponible completamente",
                f"• Retiro único con liquidez inmediata",
                f"• Flexibilidad para reinvertir o utilizar según necesidades"
            ]

        for point in analysis_points:
            elements.append(Paragraph(point, self.normal_style))

        elements.append(Spacer(1, 20))

        # Detailed Breakdown Table
        elements.append(Paragraph("📋 DESGLOSE DETALLADO", self.section_style))

        if resumen.get('tipo_retiro') == 'pension':
            elements.append(Paragraph("Detalle completo de pensiones mensuales y anuales", self.normal_style))

            breakdown_data = [
                ["Concepto", "Mensual", "Anual"],
                ["Pensión Bruta", f"${resumen.get('pension_mensual_bruta', 0):,.2f}",
                 f"${resumen.get('pension_anual_bruta', 0):,.2f}"],
                ["Impuestos", f"${resumen.get('impuesto_mensual', 0):,.2f}",
                 f"${resumen.get('impuesto_anual', 0):,.2f}"],
                ["Pensión Neta", f"${resumen.get('pension_mensual_neta', 0):,.2f}",
                 f"${resumen.get('pension_anual_neta', 0):,.2f}"]
            ]
        else:
            elements.append(Paragraph("Detalle del retiro total con impuestos", self.normal_style))

            breakdown_data = [
                ["Concepto", "Monto"],
                ["Retiro Bruto", f"${resumen.get('pension_mensual_bruta', 0):,.2f}"],
                ["Impuestos", f"${resumen.get('impuesto_mensual', 0):,.2f}"],
                ["Retiro Neto", f"${resumen.get('pension_mensual_neta', 0):,.2f}"]
            ]

        breakdown_table = Table(breakdown_data, colWidths=[4*cm, 4*cm, 4*cm] if resumen.get('tipo_retiro') == 'pension' else [6*cm, 6*cm])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.table_header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.primary_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(breakdown_table)

        # Additional information
        if resumen.get('mensaje'):
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("📝 INFORMACIÓN ADICIONAL", self.section_style))
            elements.append(Paragraph(resumen.get('mensaje', 'Cálculo completado exitosamente'), self.normal_style))

        # Footer
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=10))
        elements.append(Paragraph("Reporte generado por Simulador Financiero - Todos los cálculos son proyecciones basadas en los parámetros proporcionados", self.footer_style))
        elements.append(Paragraph(f"Página 1 - Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", self.footer_style))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_strategy_comparison_report(self, estrategias, benchmarks, analisis_riesgo, configuracion=None):
        """Generate professional PDF report for strategy comparison"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        elements = []

        # Header with branding
        header_data = [
            [Paragraph("SIMULADOR FINANCIERO", ParagraphStyle('HeaderMain',
                fontSize=18, fontName='Helvetica-Bold', textColor=self.primary_color, alignment=0)),
             Paragraph("Reporte Profesional", ParagraphStyle('HeaderSub',
                fontSize=12, fontName='Helvetica', textColor=self.secondary_color, alignment=2))]
        ]
        header_table = Table(header_data, colWidths=[10*cm, 6*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=2, color=self.secondary_color, spaceAfter=20))

        # Main Title
        elements.append(Paragraph("Comparación de Estrategias de Inversión", self.title_style))
        elements.append(Paragraph("Análisis comparativo de diferentes estrategias de inversión", self.small_style))
        elements.append(Spacer(1, 15))

        # Generation info
        info_data = [
            ["Fecha de generación:", datetime.now().strftime('%d/%m/%Y %H:%M')],
            ["Tipo de análisis:", "Comparación de estrategias de inversión"],
            ["Moneda:", "USD (Dólares Americanos)"]
        ]
        info_table = Table(info_data, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), self.primary_color),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # Executive Summary Section
        elements.append(Paragraph("📊 RESUMEN EJECUTIVO", self.section_style))
        elements.append(Paragraph("Principales indicadores de la comparación de estrategias", self.normal_style))

        # Find best performing strategy
        best_strategy = max(estrategias, key=lambda x: x.get('Capital Promedio (USD)', 0))

        # Key metrics in a highlighted box
        key_metrics_data = [
            ["Métrica", "Valor", "Interpretación"],
            ["Mejor Estrategia", best_strategy.get('Estrategia', 'N/A'),
             "Estrategia con mejor rendimiento proyectado"],
            ["Capital Máximo", f"${best_strategy.get('Capital Promedio (USD)', 0):,.2f}",
             "Capital final proyectado de la mejor estrategia"],
            ["TEA Esperada", f"{best_strategy.get('TEA Esperada (%)', 0):.2f}%",
             "Tasa efectiva anual de la mejor estrategia"],
            ["Volatilidad Promedio", f"{analisis_riesgo.get('volatilidad_promedio', 0):.2f}%",
             "Volatilidad promedio de todas las estrategias"],
            ["Probabilidad Éxito", f"{analisis_riesgo.get('probabilidad_exito', 0):.1f}%",
             "Probabilidad de superar el escenario promedio"]
        ]

        key_metrics_table = Table(key_metrics_data, colWidths=[3.5*cm, 3.5*cm, 9*cm])
        key_metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.secondary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(key_metrics_table)
        elements.append(Spacer(1, 15))

        # Strategy Comparison Table
        elements.append(Paragraph("📋 COMPARACIÓN DE ESTRATEGIAS", self.section_style))
        elements.append(Paragraph(f"Comparación detallada de {len(estrategias)} estrategias de inversión", self.normal_style))

        # Prepare table data
        table_data = [['Estrategia', 'Capital Final (USD)', 'TEA Esperada (%)', 'Volatilidad (%)', 'Ratio Sharpe']]
        for estrategia in estrategias:
            table_data.append([
                estrategia.get('Estrategia', 'N/A'),
                f"${estrategia.get('Capital Promedio (USD)', 0):,.2f}",
                f"{estrategia.get('TEA Esperada (%)', 0):.2f}%",
                f"{estrategia.get('Volatilidad (%)', 0):.2f}%",
                f"{estrategia.get('Ratio Sharpe', 0):.3f}"
            ])

        strategy_table = Table(table_data, colWidths=[3*cm, 3*cm, 2.5*cm, 2.5*cm, 2.5*cm])
        strategy_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.table_header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.primary_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(strategy_table)
        elements.append(Spacer(1, 20))

        # Benchmark Comparison
        elements.append(Paragraph("📈 COMPARACIÓN CON BENCHMARKS", self.section_style))
        elements.append(Paragraph("Comparación con índices de mercado y estrategias tradicionales", self.normal_style))

        # Prepare benchmark table
        benchmark_data = [['Benchmark', 'Capital Final (USD)', 'TEA (%)', 'Diferencia vs Mercado (%)']]
        for benchmark in benchmarks:
            diferencia = benchmark.get('Diferencia vs Mercado (%)', 0)
            benchmark_data.append([
                benchmark.get('Benchmark', 'N/A'),
                f"${benchmark.get('Capital Final (USD)', 0):,.2f}",
                f"{benchmark.get('TEA (%)', 0):.2f}%",
                f"{diferencia:+.2f}%"
            ])

        benchmark_table = Table(benchmark_data, colWidths=[3.5*cm, 3*cm, 2*cm, 3*cm])
        benchmark_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.table_header_bg),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.primary_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(benchmark_table)
        elements.append(Spacer(1, 20))

        # Risk Analysis
        elements.append(Paragraph("⚠️ ANÁLISIS DE RIESGO", self.section_style))
        elements.append(Paragraph("Evaluación de riesgos y escenarios de la comparación", self.normal_style))

        risk_data = [
            ["Métrica de Riesgo", "Valor", "Interpretación"],
            ["Volatilidad Promedio", f"{analisis_riesgo.get('volatilidad_promedio', 0):.2f}%",
             "Desviación estándar promedio de los retornos"],
            ["Mejor Escenario", f"${analisis_riesgo.get('mejor_escenario', 0):,.2f}",
             "Capital máximo posible en escenario favorable"],
            ["Peor Escenario", f"${analisis_riesgo.get('peor_escenario', 0):,.2f}",
             "Capital mínimo posible en escenario desfavorable"],
            ["Probabilidad Éxito", f"{analisis_riesgo.get('probabilidad_exito', 0):.1f}%",
             "Probabilidad de superar el rendimiento promedio"]
        ]

        risk_table = Table(risk_data, colWidths=[4*cm, 3*cm, 9*cm])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.warning_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), self.light_bg),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(risk_table)
        elements.append(Spacer(1, 20))

        # Analysis and Conclusions
        elements.append(Paragraph("💡 ANÁLISIS Y CONCLUSIONES", self.section_style))

        # Generate insights based on the data
        insights = [
            f"• La estrategia <b>{best_strategy.get('Estrategia', 'N/A')}</b> presenta el mejor rendimiento proyectado",
            f"• Capital final máximo: ${best_strategy.get('Capital Promedio (USD)', 0):,.2f}",
            f"• La volatilidad promedio del portafolio es del {analisis_riesgo.get('volatilidad_promedio', 0):.2f}%",
            f"• {len([e for e in estrategias if e.get('Ratio Sharpe', 0) > 1])} estrategias muestran ratio Sharpe superior a 1",
            f"• Probabilidad de éxito del {analisis_riesgo.get('probabilidad_exito', 0):.1f}% en superar el rendimiento promedio"
        ]

        for insight in insights:
            elements.append(Paragraph(insight, self.normal_style))

        elements.append(Spacer(1, 20))

        # Configuration Summary
        if configuracion:
            elements.append(Paragraph("🔧 CONFIGURACIÓN UTILIZADA", self.section_style))
            config_data = [
                ["Parámetro", "Valor"],
                ["Estrategias Comparadas", ", ".join(configuracion.get('estrategias_seleccionadas', []))],
                ["Frecuencia Rebalanceo", configuracion.get('frecuencia_rebalanceo', 'N/A').title()],
                ["Estrategia Personalizada", "Sí" if configuracion.get('estrategia_personalizada') else "No"]
            ]

            if configuracion.get('estrategia_personalizada'):
                custom = configuracion['estrategia_personalizada']
                config_data.extend([
                    ["Acciones (%)", f"{custom.get('stocks', 0)}%"],
                    ["Bonos (%)", f"{custom.get('bonds', 0)}%"],
                    ["Oro (%)", f"{custom.get('gold', 0)}%"],
                    ["Bienes Raíces (%)", f"{custom.get('realEstate', 0)}%"]
                ])

            config_table = Table(config_data, colWidths=[5*cm, 11*cm])
            config_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.table_header_bg),
                ('TEXTCOLOR', (0, 0), (-1, 0), self.primary_color),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(config_table)
            elements.append(Spacer(1, 20))

        # Footer
        elements.append(Spacer(1, 30))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=10))
        elements.append(Paragraph("Reporte generado por Simulador Financiero - Todos los cálculos son proyecciones basadas en los parámetros proporcionados", self.footer_style))
        elements.append(Paragraph(f"Página 1 - Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", self.footer_style))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

# Convenience functions
def generar_pdf_cartera(df, resumen, grafica_path=None):
    """Generate portfolio PDF report"""
    generator = PDFGenerator()
    return generator.generate_portfolio_report(df, resumen, grafica_path)

def generar_pdf_bono(df, resumen):
    """Generate bond PDF report"""
    generator = PDFGenerator()
    return generator.generate_bond_report(df, resumen)

def generar_pdf_jubilacion(resumen):
    """Generate retirement PDF report"""
    generator = PDFGenerator()
    return generator.generate_retirement_report(resumen)

def generar_pdf_comparacion(estrategias, benchmarks, analisis_riesgo, configuracion=None):
    """Generate strategy comparison PDF report"""
    generator = PDFGenerator()
    return generator.generate_strategy_comparison_report(estrategias, benchmarks, analisis_riesgo, configuracion)

def generar_pdf_completo(cartera_data=None, jubilacion_data=None, bono_data=None):
    """Generate complete PDF report with all modules"""
    # TODO: Implement complete report generation
    pass
