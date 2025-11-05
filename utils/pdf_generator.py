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
        """Generate PDF report for bond valuation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        # Title
        elements.append(Paragraph("Reporte de Valoración de Bonos", self.title_style))
        elements.append(Spacer(1, 12))

        # Date
        elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.normal_style))
        elements.append(Spacer(1, 20))

        # Summary
        elements.append(Paragraph("Resumen de Valoración", self.subtitle_style))

        summary_data = [
            ["Parámetro", "Valor"],
            ["Valor Nominal", f"${resumen['valor_nominal']:,.2f}"],
            ["Tasa Cupón", f"{resumen['tasa_cupon']:.2f}%"],
            ["Valor Presente Total", f"${resumen['valor_presente_total']:,.2f}"],
            ["Diferencia", f"${resumen['diferencia']:,.2f}"],
            ["Estado", resumen['estado']]
        ]

        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # Cash flows table
        elements.append(Paragraph("Flujos de Caja", self.subtitle_style))

        table_data = [df.columns.tolist()]
        for _, row in df.iterrows():
            table_data.append([
                int(row['Periodo']),
                f"${row['Flujo (USD)']:,.2f}",
                f"${row['Valor Presente (USD)']:,.2f}"
            ])

        flows_table = Table(table_data)
        flows_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
        ]))

        elements.append(flows_table)

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_retirement_report(self, resumen):
        """Generate PDF report for retirement projection"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        # Title
        elements.append(Paragraph("Reporte de Proyección de Jubilación", self.title_style))
        elements.append(Spacer(1, 12))

        # Date
        elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.normal_style))
        elements.append(Spacer(1, 20))

        # Summary
        elements.append(Paragraph("Resumen de Jubilación", self.subtitle_style))

        summary_data = [
            ["Parámetro", "Valor"],
            ["Tipo de Retiro", "Pensión Mensual" if resumen.get('tipo_retiro') == 'pension' else "Retiro Total"],
            ["Tipo de Impuesto", resumen.get('tipo_impuesto', '').title()],
            ["Capital Inicial", f"${resumen.get('capital_inicial', 0):,.2f}"],
            ["TEA de Retiro", f"{resumen.get('tea_retiro', 0):.2f}%"],
        ]

        if resumen.get('tipo_retiro') == 'pension':
            summary_data.extend([
                ["Años de Retiro", resumen.get('años_retiro', 0)],
                ["Pensión Mensual Bruta", f"${resumen.get('pension_mensual_bruta', 0):,.2f}"],
                ["Impuesto Mensual", f"${resumen.get('impuesto_mensual', 0):,.2f}"],
                ["Pensión Mensual Neta", f"${resumen.get('pension_mensual_neta', 0):,.2f}"],
                ["Pensión Anual Bruta", f"${resumen.get('pension_anual_bruta', 0):,.2f}"],
                ["Impuesto Anual", f"${resumen.get('impuesto_anual', 0):,.2f}"],
                ["Pensión Anual Neta", f"${resumen.get('pension_anual_neta', 0):,.2f}"],
            ])
        else:
            summary_data.extend([
                ["Retiro Total Bruto", f"${resumen.get('pension_mensual_bruta', 0):,.2f}"],
                ["Impuesto Total", f"${resumen.get('impuesto_mensual', 0):,.2f}"],
                ["Retiro Total Neto", f"${resumen.get('pension_mensual_neta', 0):,.2f}"],
            ])

        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # Additional information
        elements.append(Paragraph("Información Adicional", self.subtitle_style))
        elements.append(Paragraph(f"Mensaje: {resumen.get('mensaje', 'Cálculo completado exitosamente')}", self.normal_style))

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

def generar_pdf_completo(cartera_data=None, jubilacion_data=None, bono_data=None):
    """Generate complete PDF report with all modules"""
    # TODO: Implement complete report generation
    pass
