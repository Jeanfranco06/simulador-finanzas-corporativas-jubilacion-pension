# SIMULADOR FINANCIERO DE JUBILACIÓN
## Proyecto Completo - Finanzas Corporativas

---

## 📦 CONTENIDO DEL PAQUETE

Este paquete contiene el proyecto completo del Simulador Financiero de Jubilación desarrollado en Streamlit, siguiendo todas las especificaciones del examen parcial de Finanzas Corporativas.

### Archivos y Carpetas Incluidos:

```
simulador_financiero/
│
├── 📄 app.py                          # Aplicación principal Streamlit
├── 📄 requirements.txt                # Dependencias del proyecto
├── 📄 README.md                       # Documentación principal
├── 📄 INSTALACION.md                  # Guía de instalación detallada
├── 📄 EJEMPLOS.md                     # Ejemplos de uso prácticos
├── 🚀 run.bat                         # Script inicio Windows
├── 🚀 run.sh                          # Script inicio Linux/Mac
├── 📄 generar_manual.py               # Script para generar manual
│
├── 📁 utils/                          # Módulos de utilidades
│   ├── __init__.py
│   ├── calculos_financieros.py       # Todas las fórmulas financieras
│   ├── validaciones.py               # Validaciones de entrada
│   └── exportar_pdf.py               # Generación de PDFs
│
├── 📁 assets/                         # Recursos estáticos
│   └── styles.css                    # Estilos personalizados
│
├── 📁 docs/                           # Documentación
│   └── Manual_Usuario.pdf            # Manual completo en PDF
│
└── 📁 .streamlit/                     # Configuración
    └── config.toml                   # Configuración de Streamlit
```

---

## ✅ CUMPLIMIENTO DE REQUERIMIENTOS

### MÓDULOS IMPLEMENTADOS:

#### ✅ Módulo A - Crecimiento de Cartera
- ✓ Cálculo con depósito único inicial
- ✓ Cálculo con aportes periódicos (mensual, bimestral, trimestral, cuatrimestral, semestral, anual)
- ✓ Interés compuesto con TEA
- ✓ Conversión automática de tasas equivalentes
- ✓ Gráfica interactiva del crecimiento
- ✓ Tabla detallada periodo por periodo

#### ✅ Módulo B - Proyección de Jubilación
- ✓ Usa capital acumulado del Módulo A
- ✓ Opción de Cobro Total
- ✓ Opción de Pensión Mensual
- ✓ Cálculo de impuestos (29.5% extranjera / 5% local)
- ✓ Pensión mensual estimada en USD
- ✓ Comparador de escenarios (edades y tasas)
- ✓ Resultados detallados en USD

#### ✅ Módulo C - Valoración de Bonos
- ✓ Cálculo del valor presente
- ✓ Flujos periódicos (mensual, bimestral, trimestral, cuatrimestral, semestral, anual)
- ✓ Valor descontado de cada flujo
- ✓ Valor presente total
- ✓ Tabla detallada de flujos
- ✓ Gráficas de comparación

---

## 🎯 FUNCIONALIDADES IMPLEMENTADAS

### Entradas (UI):
✅ Edad actual y edad de jubilación
✅ Monto inicial en USD
✅ Aporte periódico en USD
✅ Frecuencia de aportes (6 opciones)
✅ Plazo en años o por edad
✅ TEA (0% - 50%)
✅ Tipo de impuesto (2 opciones)
✅ Datos completos para bonos
✅ Todos los campos con ayuda contextual (?)

### Salidas Esperadas:
✅ Reporte detallado del crecimiento
✅ Gráficas interactivas
✅ Valor actual del bono
✅ Resumen en USD con impuestos
✅ Pensión mensual estimada
✅ Comparación de escenarios
✅ Exportación a PDF

### Validaciones:
✅ Montos no negativos
✅ TEA entre 0% y 50%
✅ Mensajes claros de error
✅ Conversión automática de tasas
✅ Valores en USD
✅ Cifras redondeadas a 2 decimales

### Requerimientos No Funcionales:
✅ Interfaz amigable en español
✅ Diseño ordenado y limpio
✅ Ayuda contextual en cada campo
✅ Exportación a PDF
✅ Listo para usuarios no técnicos

---

## 🚀 INSTALACIÓN RÁPIDA

### Windows:
1. Descomprimir el archivo ZIP
2. Doble clic en `run.bat`
3. ¡Listo!

### Linux/Mac:
1. Descomprimir el archivo ZIP
2. En terminal: `./run.sh`
3. ¡Listo!

### Manual:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📖 DOCUMENTACIÓN INCLUIDA

1. **Manual de Usuario (PDF):** 
   - Ubicación: `docs/Manual_Usuario.pdf`
   - 30+ páginas de documentación completa
   - Instrucciones paso a paso
   - Preguntas frecuentes
   - Información de contacto

2. **Guía de Instalación:**
   - Archivo: `INSTALACION.md`
   - Requisitos del sistema
   - Instalación paso a paso
   - Solución de problemas

3. **Ejemplos de Uso:**
   - Archivo: `EJEMPLOS.md`
   - Casos prácticos para cada módulo
   - Ejercicios propuestos
   - Caso completo de planificación

4. **README Principal:**
   - Archivo: `README.md`
   - Vista general del proyecto
   - Características principales
   - Estructura del proyecto

---

## 💻 TECNOLOGÍAS UTILIZADAS

- **Python 3.8+**: Lenguaje de programación
- **Streamlit**: Framework para la interfaz web
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **Plotly**: Gráficas interactivas
- **ReportLab**: Generación de PDFs
- **Matplotlib**: Gráficas adicionales

---

## 📊 FÓRMULAS IMPLEMENTADAS

### Interés Compuesto:
```
VF = VP × (1 + i)^n + PMT × [((1 + i)^n - 1) / i]
```

### Tasa Equivalente:
```
i_periodo = (1 + TEA)^(1/n) - 1
```

### Pensión Mensual (Anualidad):
```
PMT = PV × [r(1+r)^n] / [(1+r)^n - 1]
```

### Valor Presente del Bono:
```
VP = Σ [Cupón / (1 + r)^t] + [VN / (1 + r)^n]
```

---

## 🎨 CARACTERÍSTICAS DE LA INTERFAZ

- **Diseño Moderno:** Colores corporativos azules
- **Responsive:** Se adapta a diferentes tamaños de pantalla
- **Intuitivo:** Navegación por pestañas clara
- **Validación en Tiempo Real:** Mensajes de error inmediatos
- **Gráficas Interactivas:** Zoom, pan, descarga de imágenes
- **Ayuda Contextual:** Tooltip en cada campo
- **Métricas Destacadas:** Resumen visual de resultados
- **Tablas Expandibles:** Para no saturar la pantalla
- **Exportación Fácil:** Un clic para generar PDF

---

## ✨ CARACTERÍSTICAS DESTACADAS

### 1. Cálculos Precisos
- Todas las fórmulas financieras implementadas correctamente
- Conversión automática de tasas equivalentes
- Precisión de 2 decimales en todos los resultados

### 2. Validaciones Robustas
- Validación de rangos (TEA 0%-50%)
- Validación de coherencia (edad retiro > edad actual)
- Mensajes de error claros y específicos

### 3. Visualización Profesional
- Gráficas interactivas con Plotly
- Tablas ordenadas y legibles
- Métricas destacadas con deltas

### 4. Exportación Completa
- PDFs con diseño profesional
- Incluye gráficas en alta resolución
- Marca de fecha y hora
- Listo para imprimir o compartir

### 5. Experiencia de Usuario
- Interfaz en español
- Sin conocimientos técnicos requeridos
- Flujo lógico entre módulos
- Retroalimentación inmediata

---

## 🧪 CASOS DE PRUEBA SUGERIDOS

### Prueba 1: Aportes Mensuales Básicos
- Monto Inicial: $5,000
- Aporte Mensual: $500
- TEA: 8%
- Años: 30
- **Resultado esperado:** ~$745,000 USD

### Prueba 2: Valoración de Bono con Prima
- Valor Nominal: $1,000
- Tasa Cupón: 8%
- Frecuencia: Semestral
- Plazo: 5 años
- TEA Retorno: 6%
- **Resultado esperado:** VP > $1,000 (Prima)

### Prueba 3: Pensión con Impuesto Alto
- Capital: $500,000
- Ganancia: $300,000
- Impuesto: 29.5% Extranjera
- Años Retiro: 25
- **Resultado esperado:** Pensión ~$2,740 USD/mes

---

## 📝 NOTAS IMPORTANTES

1. **Primera Ejecución:** Puede tomar 2-3 minutos instalar dependencias
2. **Requisitos:** Python 3.8+ debe estar instalado
3. **Puerto:** La aplicación usa el puerto 8501 por defecto
4. **Navegador:** Compatible con Chrome, Firefox, Safari, Edge
5. **PDFs:** Se descargan automáticamente a la carpeta de descargas

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### "Python no encontrado"
→ Instalar Python desde python.org

### "Módulo no encontrado"
→ Ejecutar: `pip install -r requirements.txt`

### "Puerto en uso"
→ Cerrar otras instancias o usar: `streamlit run app.py --server.port 8502`

### "No se genera el PDF"
→ Verificar que ReportLab esté instalado: `pip install reportlab`

---

## 🎓 ENTREGABLES DEL PROYECTO

✅ **1. Código Fuente Completo**
   - Todos los archivos .py
   - Estructura modular y documentada
   - Comentarios en código

✅ **2. Manual de Usuario (PDF)**
   - Ubicación: docs/Manual_Usuario.pdf
   - 30+ páginas
   - Para usuario no técnico

✅ **3. Aplicación Funcional**
   - Ejecutable via scripts run.bat/run.sh
   - Interface web en Streamlit
   - Lista para demostración

✅ **4. Documentación Adicional**
   - README.md
   - INSTALACION.md
   - EJEMPLOS.md

---

## 🎯 LISTO PARA DEMOSTRACIÓN

El proyecto está completamente listo para la demostración en clase:

1. ✅ Se puede abrir desde archivo descargado
2. ✅ Funciona en entorno limpio
3. ✅ Puede realizar simulación con aportes mensuales
4. ✅ Puede calcular valor de un bono
5. ✅ Puede proyectar pensión mensual
6. ✅ Puede exportar resultados a PDF

---

## 📞 INFORMACIÓN DE CONTACTO

Para soporte o consultas sobre el proyecto:

**Email:** soporte@simuladorfinanciero.com
**Proyecto:** Examen Parcial - Unidad II
**Curso:** Finanzas Corporativas
**Año:** 2025

---

## 📄 LICENCIA

© 2025 Simulador Financiero de Jubilación
Proyecto académico - Finanzas Corporativas
Todos los derechos reservados.

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de la entrega, verificar:

- [x] Código fuente completo
- [x] Todos los módulos funcionando (A, B, C)
- [x] Manual de usuario en PDF
- [x] Scripts de ejecución (Windows y Linux)
- [x] Validaciones implementadas
- [x] Exportación a PDF funcional
- [x] Gráficas interactivas
- [x] Interfaz en español
- [x] Ayuda contextual en campos
- [x] Cálculos precisos (2 decimales)
- [x] Valores en USD
- [x] Conversión de tasas automática
- [x] Diseño profesional
- [x] Listo para demostración

---

## 🎉 ¡PROYECTO COMPLETO!

Este proyecto cumple al 100% con todos los requerimientos del examen parcial:
- ✅ Módulo A completo
- ✅ Módulo B completo  
- ✅ Módulo C completo
- ✅ Validaciones completas
- ✅ Exportación a PDF
- ✅ Manual de usuario
- ✅ Interfaz profesional
- ✅ Listo para demo

**¡Buena suerte en tu presentación!** 🚀
