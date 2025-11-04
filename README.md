# Simulador Financiero de Jubilación

Herramienta profesional para proyección de jubilación y valoración de bonos desarrollada con Flask.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚀 Despliegue en Render

Esta aplicación está configurada para desplegarse fácilmente en [Render](https://render.com).

### Despliegue Automático

1. Haz clic en el botón "Deploy to Render" arriba
2. Conecta tu repositorio de GitHub
3. Render detectará automáticamente la configuración en `render.yaml`
4. ¡Tu aplicación estará lista en minutos!

### Despliegue Manual

1. Crea una cuenta en [Render](https://render.com)
2. Conecta tu repositorio
3. Configura el servicio web con:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

## 📋 Características

- **🎯 Módulo A**: Crecimiento de cartera con aportes periódicos e interés compuesto
- **🏠 Módulo B**: Proyección de retiro y cálculo de pensión mensual
- **💰 Módulo C**: Valoración profesional de bonos con flujos de efectivo
- **📊 Gráficas Interactivas**: Visualización de datos con Chart.js
- **📄 Exportación PDF**: Reportes profesionales descargables
- **📱 Responsive**: Diseño adaptativo para todos los dispositivos
- **🎨 UI Moderna**: Interfaz elegante con Tailwind CSS

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Gráficas**: Chart.js
- **Análisis de Datos**: Pandas, NumPy
- **PDF Generation**: ReportLab
- **Deployment**: Render (WSGI con Gunicorn)

## 🏗️ Estructura del Proyecto

```
simulador_financiero/
├── app.py                          # Aplicación principal Flask
├── config.py                       # Configuración de la aplicación
├── requirements.txt                # Dependencias Python
├── render.yaml                     # Configuración de despliegue Render
├── README.md                       # Este archivo
├── app/
│   ├── __init__.py                # Inicialización de la app Flask
│   ├── routes.py                  # Definición de rutas
│   ├── forms.py                   # Formularios WTForms
│   ├── models.py                  # Modelos de datos
│   ├── static/                    # Archivos estáticos
│   │   ├── css/style.css         # Estilos personalizados
│   │   └── js/graficas.js        # Scripts JavaScript
│   └── templates/                 # Plantillas Jinja2
│       ├── base.html             # Plantilla base
│       ├── index.html            # Página principal
│       ├── cartera.html          # Módulo A
│       ├── jubilacion.html       # Módulo B
│       ├── bonos.html            # Módulo C
│       └── resultado.html        # Resultados
├── utils/
│   ├── __init__.py
│   ├── calculos_financieros.py   # Funciones de cálculo financiero
│   ├── validaciones.py           # Validaciones de entrada
│   ├── pdf_generator.py          # Generación de PDFs
│   └── graficos.py               # Utilidades de gráficos
├── docs/
│   └── Manual_Usuario.pdf        # Manual de usuario
└── assets/                       # Recursos adicionales
```

## 💻 Desarrollo Local

### Prerrequisitos

- Python 3.8+
- pip

### Instalación

```bash
# Clona el repositorio
git clone <tu-repositorio>
cd simulador_financiero

# Instala dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
# Modo desarrollo
python app.py

# O usando Flask CLI
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

La aplicación estará disponible en `http://localhost:5000`

## 📊 Módulos Disponibles

### Módulo A: Crecimiento de Cartera
- Depósito inicial único
- Aportes periódicos (mensual, trimestral, etc.)
- Cálculo de interés compuesto
- Visualización gráfica del crecimiento
- Tabla detallada de periodos

### Módulo B: Proyección de Jubilación
- Cálculo de pensión mensual
- Consideraciones fiscales (5% bolsa local, 29.5% fuente extranjera)
- Escenarios comparativos
- Proyección a largo plazo

### Módulo C: Valoración de Bonos
- Valor presente de flujos de efectivo
- Análisis de prima/descuento
- Cupones periódicos
- Tabla de amortización

## 🔧 Configuración

La aplicación utiliza variables de entorno para configuración:

- `FLASK_ENV`: Entorno de ejecución (`development` o `production`)
- `SECRET_KEY`: Clave secreta para sesiones Flask (generada automáticamente en Render)

## 📈 Moneda

Todos los cálculos se realizan en **Dólares Estadounidenses (USD)**.

## 📄 Licencia

Proyecto académico - Finanzas Corporativas - Unidad II

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Para soporte técnico o preguntas sobre la aplicación, por favor revisa la documentación en la carpeta `docs/` o contacta al equipo de desarrollo.
