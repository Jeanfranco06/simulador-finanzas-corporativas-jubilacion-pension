"""
Simulador Financiero de Jubilación
Aplicación Flask para proyección de jubilación y valoración de bonos

Autor: Proyecto Finanzas Corporativas
Fecha: 2025
"""

from app import create_app

# Create Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the application in debug mode for development
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
