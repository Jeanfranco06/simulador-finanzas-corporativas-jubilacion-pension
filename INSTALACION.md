# INSTRUCCIONES DE INSTALACIÓN Y EJECUCIÓN
## Simulador Financiero de Jubilación

---

## 📋 REQUISITOS PREVIOS

Antes de instalar el simulador, asegúrese de tener instalado:

1. **Python 3.8 o superior**
   - Descarga: https://www.python.org/downloads/
   - Durante la instalación, marque "Add Python to PATH"

2. **pip (Administrador de paquetes de Python)**
   - Se instala automáticamente con Python
   - Verifique ejecutando: `pip --version`

---

## 🚀 INSTALACIÓN

### Opción 1: Instalación Automática (Recomendada)

#### Windows:
1. Abra la carpeta del proyecto
2. Haga doble clic en el archivo `run.bat`
3. El script instalará automáticamente las dependencias y ejecutará la aplicación

#### Linux/Mac:
1. Abra una terminal en la carpeta del proyecto
2. Ejecute: `./run.sh`
3. El script instalará automáticamente las dependencias y ejecutará la aplicación

### Opción 2: Instalación Manual

1. Abra una terminal o símbolo del sistema
2. Navegue a la carpeta del proyecto:
   ```bash
   cd ruta/a/simulador_financiero
   ```

3. Instale las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecute la aplicación:
   ```bash
   streamlit run app.py
   ```

---

## 💻 EJECUCIÓN DE LA APLICACIÓN

### Primera Vez:
- El sistema instalará todas las librerías necesarias
- Puede tomar 2-3 minutos dependiendo de su conexión

### Ejecuciones Posteriores:
- La aplicación iniciará inmediatamente
- Se abrirá automáticamente en su navegador predeterminado
- URL por defecto: http://localhost:8501

### Si no se abre el navegador automáticamente:
1. Abra su navegador web
2. Vaya a: http://localhost:8501

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "Python no está instalado"
**Solución:** 
- Descargue e instale Python desde python.org
- Asegúrese de marcar "Add Python to PATH" durante la instalación
- Reinicie su computadora después de la instalación

### Error: "pip no está disponible"
**Solución:**
```bash
python -m ensurepip --upgrade
```

### Error: "No se pueden instalar las dependencias"
**Solución:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Error: "Puerto 8501 ya está en uso"
**Solución:**
- Cierre otras instancias de Streamlit
- O ejecute en otro puerto:
```bash
streamlit run app.py --server.port 8502
```

### La aplicación no responde o es muy lenta
**Solución:**
- Cierre pestañas innecesarias del navegador
- Reinicie la aplicación
- Verifique que su computadora cumpla los requisitos mínimos

---

## 📁 ESTRUCTURA DEL PROYECTO

```
simulador_financiero/
│
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias
├── run.bat                         # Script de inicio (Windows)
├── run.sh                          # Script de inicio (Linux/Mac)
├── README.md                       # Documentación principal
├── INSTALACION.md                  # Este archivo
│
├── utils/                          # Módulos de utilidades
│   ├── __init__.py
│   ├── calculos_financieros.py    # Cálculos financieros
│   ├── validaciones.py            # Validaciones
│   └── exportar_pdf.py            # Exportación a PDF
│
├── assets/                         # Recursos estáticos
│   └── styles.css                 # Estilos personalizados
│
└── docs/                           # Documentación
    └── Manual_Usuario.pdf         # Manual de usuario
```

---

## 📖 USO DE LA APLICACIÓN

### Inicio Rápido:
1. Ejecute la aplicación
2. Vaya a la pestaña "Módulo A: Cartera"
3. Complete los datos solicitados
4. Haga clic en "Calcular Proyección"
5. Revise los resultados y gráficas
6. Vaya a "Módulo B: Jubilación" para calcular su pensión
7. Opcional: Use "Módulo C: Bonos" para valorar bonos
8. Exporte sus resultados a PDF

### Consulte el Manual de Usuario:
- Ubicación: `docs/Manual_Usuario.pdf`
- Contiene instrucciones detalladas de cada módulo
- Incluye ejemplos y casos de uso

---

## 🔐 PRIVACIDAD Y SEGURIDAD

- Todos los cálculos se realizan localmente en su computadora
- No se envía información a servidores externos
- No se requiere conexión a Internet después de la instalación
- Sus datos no son almacenados permanentemente

---

## 💾 EXPORTACIÓN DE RESULTADOS

Los reportes PDF se generan y descargan automáticamente a su carpeta de descargas.

Para cambiar la ubicación:
- Configure su navegador para preguntar dónde guardar archivos
- O cambie la carpeta de descargas predeterminada

---

## 🔄 ACTUALIZACIONES

Para actualizar el simulador:
1. Descargue la nueva versión
2. Reemplace los archivos antiguos
3. Ejecute nuevamente `pip install -r requirements.txt`

---

## 📞 SOPORTE TÉCNICO

Si tiene problemas no resueltos en esta guía:

**Email:** soporte@simuladorfinanciero.com
**Teléfono:** +51 (01) 123-4567
**Horario:** Lunes a Viernes, 9:00 AM - 6:00 PM

---

## 📄 LICENCIA

© 2025 Simulador Financiero de Jubilación
Todos los derechos reservados.

---

## ✅ VERIFICACIÓN DE INSTALACIÓN

Para verificar que todo está correctamente instalado:

```bash
python --version          # Debe mostrar Python 3.8+
pip --version             # Debe mostrar pip instalado
streamlit --version       # Debe mostrar Streamlit instalado
```

---

**¡Gracias por usar el Simulador Financiero de Jubilación!**
