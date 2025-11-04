"""
Graphics generation utilities for the Financial Simulator
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import seaborn as sns
import io
import base64
from typing import Optional, Dict, Any

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class GraficosGenerator:
    """Class for generating charts and graphs"""

    def __init__(self):
        self.fig_size = (10, 6)
        self.dpi = 100

    def generar_grafica_cartera(self, df, titulo="Evolución de la Cartera"):
        """
        Generate portfolio growth chart

        Args:
            df: DataFrame with portfolio data
            titulo: Chart title

        Returns:
            Base64 encoded image string
        """
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)

        # Plot data
        ax.plot(df['Periodo'], df['Saldo Final (USD)'], label='Saldo Total', linewidth=2, marker='o', markersize=3)
        ax.plot(df['Periodo'], df['Aportes Acumulados (USD)'], label='Aportes Acumulados', linewidth=2, linestyle='--', marker='s', markersize=3)

        # Formatting
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Periodo', fontsize=12)
        ax.set_ylabel('Monto (USD)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Tight layout
        plt.tight_layout()

        # Convert to base64
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close(fig)

        return f"data:image/png;base64,{image_base64}"

    def generar_grafica_bonos(self, df, titulo="Flujos del Bono"):
        """
        Generate bond cash flows chart

        Args:
            df: DataFrame with bond data
            titulo: Chart title

        Returns:
            Base64 encoded image string
        """
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)

        # Create bar chart
        bar_width = 0.35
        periods = df['Periodo']

        bars1 = ax.bar(periods - bar_width/2, df['Flujo (USD)'], bar_width,
                      label='Flujo Nominal', alpha=0.8, color='skyblue')
        bars2 = ax.bar(periods + bar_width/2, df['Valor Presente (USD)'], bar_width,
                      label='Valor Presente', alpha=0.8, color='salmon')

        # Formatting
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Periodo', fontsize=12)
        ax.set_ylabel('Monto (USD)', fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')

        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Add value labels on bars
        def add_value_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'${height:,.0f}', ha='center', va='bottom', fontsize=8)

        add_value_labels(bars1)
        add_value_labels(bars2)

        # Tight layout
        plt.tight_layout()

        # Convert to base64
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close(fig)

        return f"data:image/png;base64,{image_base64}"

    def generar_grafica_jubilacion(self, datos_jubilacion, titulo="Proyección de Jubilación"):
        """
        Generate retirement projection chart

        Args:
            datos_jubilacion: Dictionary with retirement data
            titulo: Chart title

        Returns:
            Base64 encoded image string
        """
        # Placeholder for retirement chart
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=self.dpi)

        # This would be implemented when retirement calculations are complete
        ax.text(0.5, 0.5, 'Gráfica de Jubilación\n(En desarrollo)',
               transform=ax.transAxes, ha='center', va='center',
               fontsize=14, fontweight='bold')

        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        # Convert to base64
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close(fig)

        return f"data:image/png;base64,{image_base64}"

# Convenience functions
def generar_grafica_cartera(df, titulo="Evolución de la Cartera"):
    """Generate portfolio chart"""
    generator = GraficosGenerator()
    return generator.generar_grafica_cartera(df, titulo)

def generar_grafica_bonos(df, titulo="Flujos del Bono"):
    """Generate bond chart"""
    generator = GraficosGenerator()
    return generator.generar_grafica_bonos(df, titulo)

def generar_grafica_jubilacion(datos, titulo="Proyección de Jubilación"):
    """Generate retirement chart"""
    generator = GraficosGenerator()
    return generator.generar_grafica_jubilacion(datos, titulo)
