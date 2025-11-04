"""
PDF generation utilities for the Financial Simulator
"""
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
from datetime import datetime

class PDFGenerator:
    """Class for generating PDF reports"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        """Setup custom styles for the PDF"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center
        )

        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
        )

        self.normal_style = self.styles['Normal']
        self.normal_style.fontSize = 10

    def generate_portfolio_report(self, df, resumen, grafica_path=None):
        """Generate PDF report for portfolio simulation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        # Title
        elements.append(Paragraph("Reporte de Simulación de Cartera", self.title_style))
        elements.append(Spacer(1, 12))

        # Date
        elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.normal_style))
        elements.append(Spacer(1, 20))

        # Summary section
        elements.append(Paragraph("Resumen Ejecutivo", self.subtitle_style))

        summary_data = [
            ["Parámetro", "Valor"],
            ["Monto Inicial", f"${resumen['Monto Inicial']:,.2f}"],
            ["Aporte Periódico", f"${resumen['Aporte Periódico']:,.2f}"],
            ["Frecuencia", resumen['Frecuencia']],
            ["Años", resumen['Años']],
            ["TEA", f"{resumen['TEA']:.2f}%"],
            ["Capital Final", f"${resumen['Capital Final']:,.2f}"],
            ["Aportes Totales", f"${resumen['Aportes Totales']:,.2f}"],
            ["Ganancia Bruta", f"${resumen['Ganancia Bruta']:,.2f}"],
            ["Rentabilidad", f"{resumen['Rentabilidad']:.2f}%"]
        ]

        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # Chart
        if grafica_path:
            try:
                elements.append(Paragraph("Evolución de la Cartera", self.subtitle_style))
                img = Image(grafica_path, 6*inch, 4*inch)
                elements.append(img)
                elements.append(Spacer(1, 20))
            except:
                pass

        # Detailed table
        elements.append(Paragraph("Detalle por Periodo", self.subtitle_style))

        # Convert DataFrame to table data
        table_data = [df.columns.tolist()]  # Headers
        for _, row in df.iterrows():
            table_data.append([
                int(row['Periodo']),
                f"${row['Saldo Inicial']:,.2f}",
                f"${row['Aportes']:,.2f}",
                f"${row['Interés']:,.2f}",
                f"${row['Saldo Final']:,.2f}",
                f"${row['Aportes Acumulados']:,.2f}"
            ])

        # Create table with pagination if needed
        detail_table = Table(table_data)
        detail_table.setStyle(TableStyle([
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

        elements.append(detail_table)

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

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
            ["Valor Nominal", f"${resumen['Valor Nominal']:,.2f}"],
            ["Tasa Cupón", f"{resumen['Tasa Cupón']:.2f}%"],
            ["Frecuencia de Pago", resumen['Frecuencia de Pago']],
            ["Años al Vencimiento", resumen['Años al Vencimiento']],
            ["TEA Retorno", f"{resumen['TEA Retorno']:.2f}%"],
            ["Valor Presente Total", f"${resumen['Valor Presente']:,.2f}"],
            ["Diferencia", f"${resumen['Diferencia']:,.2f}"],
            ["Estado", resumen['Estado']]
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

# Convenience functions
def generar_pdf_cartera(df, resumen, grafica_path=None):
    """Generate portfolio PDF report"""
    generator = PDFGenerator()
    return generator.generate_portfolio_report(df, resumen, grafica_path)

def generar_pdf_bono(df, resumen):
    """Generate bond PDF report"""
    generator = PDFGenerator()
    return generator.generate_bond_report(df, resumen)

def generar_pdf_completo(cartera_data=None, jubilacion_data=None, bono_data=None):
    """Generate complete PDF report with all modules"""
    # TODO: Implement complete report generation
    pass
