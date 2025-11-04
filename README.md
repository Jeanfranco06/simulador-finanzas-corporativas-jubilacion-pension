# Simulador Financiero de Jubilación

Sistema de cálculo financiero para proyección de jubilación y valoración de bonos.

## Estructura del Proyecto

```
simulador_financiero/
├── app.py                          # Aplicación principal Streamlit
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
├── utils/
│   ├── __init__.py
│   ├── calculos_financieros.py    # Funciones de cálculo
│   ├── validaciones.py            # Validaciones de entrada
│   └── exportar_pdf.py            # Generación de PDFs
├── assets/
│   └── styles.css                 # Estilos personalizados
└── docs/
    └── Manual_Usuario.pdf         # Manual de usuario
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Características

- **Módulo A**: Crecimiento de cartera con aportes periódicos
- **Módulo B**: Proyección de retiro y pensión mensual
- **Módulo C**: Valoración de bonos
- **Exportación**: Generación de reportes en PDF
