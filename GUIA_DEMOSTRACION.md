# 🎓 GUÍA PARA LA DEMOSTRACIÓN EN CLASE
## Simulador Financiero de Jubilación

---

## 📋 PREPARACIÓN ANTES DE LA CLASE

### 1. Verificar Instalación (Hacer en casa)
```bash
# Verificar Python
python --version    # Debe mostrar 3.8+

# Instalar dependencias
pip install -r requirements.txt

# Probar ejecución
streamlit run app.py
```

### 2. Preparar el Entorno
- ✅ Tener el proyecto en una USB o descargado en la PC
- ✅ Verificar que Python está instalado
- ✅ Tener los datos de prueba listos (ver abajo)
- ✅ Revisar que el navegador funciona correctamente

---

## 🎯 PASOS PARA LA DEMOSTRACIÓN (5-10 minutos)

### PASO 1: Abrir la Aplicación (30 segundos)

**En Windows:**
1. Descomprimir el ZIP
2. Hacer doble clic en `run.bat`
3. Esperar que se abra el navegador

**En Linux/Mac:**
```bash
cd simulador_financiero
./run.sh
```

**Si hay problemas:**
```bash
streamlit run app.py
```

---

### PASO 2: Mostrar la Interfaz Inicial (30 segundos)

1. Explicar brevemente la pantalla de inicio
2. Mostrar las 4 pestañas principales
3. Mencionar la barra lateral con información

**Qué decir:**
> "El simulador tiene 3 módulos principales: Módulo A para simular el crecimiento de la cartera, Módulo B para calcular la pensión de jubilación, y Módulo C para valorar bonos. Todo está en dólares y tiene validaciones automáticas."

---

### PASO 3: Demostración Módulo A - Cartera (2-3 minutos)

**Ir a la pestaña "Módulo A: Cartera"**

**Datos de prueba proporcionados por el docente (usar los que él indique):**

*Ejemplo de datos que podrían darte:*
- Edad Actual: 30 años
- Monto Inicial: $5,000 USD
- Aporte Periódico: $500 USD
- Frecuencia: Mensual
- Plazo: 35 años (o Edad de Jubilación: 65 años)
- TEA: 8%

**Procedimiento:**
1. Llenar el formulario con los datos
2. Hacer clic en "Calcular Proyección"
3. Mostrar los resultados:
   - Capital Final acumulado
   - Aportes Totales
   - Ganancia Bruta
   - Rentabilidad

4. Explicar la gráfica:
   - Línea azul: Saldo total
   - Línea roja punteada: Aportes acumulados
   - Área sombreada: Ganancia por intereses

5. Expandir "Ver Detalle Completo" brevemente

**Qué decir:**
> "Como pueden ver, con aportes mensuales de $500 durante 35 años a una tasa del 8% anual, acumulamos aproximadamente [X] dólares. Los aportes totales fueron [Y], y la ganancia por intereses es de [Z]. Esto demuestra el poder del interés compuesto a largo plazo."

---

### PASO 4: Demostración Módulo B - Jubilación (2 minutos)

**Ir a la pestaña "Módulo B: Jubilación"**

**Notar:** El capital del Módulo A se transfiere automáticamente

**Datos de prueba:**
- Tipo de Retiro: Pensión Mensual
- Tipo de Impuesto: 29.5% Fuente Extranjera
- Años Esperados de Retiro: 25 años
- Usar la misma TEA: ✓ (marcado)

**Procedimiento:**
1. Seleccionar "Pensión Mensual"
2. Elegir tipo de impuesto
3. Configurar años de retiro
4. Hacer clic en "Calcular Jubilación"
5. Mostrar resultados:
   - Capital Acumulado
   - Impuesto calculado
   - Capital Neto
   - Pensión Mensual en USD

**Qué decir:**
> "Del capital acumulado, se descuenta el impuesto del 29.5% sobre las ganancias, quedándonos con un capital neto de [X]. Con este monto, y considerando que seguiremos obteniendo rendimientos durante el retiro, podemos recibir una pensión mensual de aproximadamente [Y] dólares durante 25 años."

---

### PASO 5: Demostración Módulo C - Bonos (2 minutos)

**Ir a la pestaña "Módulo C: Bonos"**

**Datos de prueba proporcionados por el docente:**

*Ejemplo:*
- Valor Nominal: $1,000 USD
- Tasa Cupón Anual: 5%
- Frecuencia de Pago: Semestral
- Plazo: 5 años
- TEA Retorno Esperada: 6%

**Procedimiento:**
1. Llenar los datos del bono
2. Hacer clic en "Valorar Bono"
3. Mostrar resultados:
   - Valor Presente calculado
   - Si cotiza con prima, descuento o a la par
   - Interpretación automática

4. Mostrar la gráfica de flujos:
   - Barras celestes: Flujos nominales
   - Barras azules: Valores presentes

5. Expandir tabla de flujos brevemente

**Qué decir:**
> "Este bono tiene un valor nominal de $1,000 y paga cupones del 5% semestralmente. Como la tasa de retorno que requerimos es del 6%, mayor al cupón, el bono cotiza con descuento, es decir, vale menos que su valor nominal. Su valor presente es de [X] dólares."

---

### PASO 6: Exportar a PDF (1 minuto)

**En cualquier módulo que tenga resultados:**

1. Hacer clic en "Exportar a PDF"
2. Hacer clic en "Descargar PDF"
3. Abrir el PDF descargado y mostrar brevemente:
   - Diseño profesional
   - Gráficas incluidas
   - Tablas detalladas
   - Fecha de generación

**Qué decir:**
> "Todos los cálculos pueden exportarse a PDF con un diseño profesional, incluyendo las gráficas y tablas detalladas. Esto permite compartir los resultados con clientes o guardar los análisis."

---

## 💡 PUNTOS CLAVE A MENCIONAR

Durante la demostración, asegúrate de mencionar:

1. **Validaciones Automáticas:**
   > "El sistema valida que las tasas estén entre 0% y 50%, que los montos no sean negativos, y que la edad de retiro sea coherente."

2. **Conversión de Tasas:**
   > "El sistema convierte automáticamente la TEA a la tasa periódica correspondiente usando la fórmula de tasas equivalentes."

3. **Todos los Valores en USD:**
   > "Todos los cálculos y resultados están en dólares estadounidenses."

4. **Interfaz Amigable:**
   > "La interfaz está diseñada para usuarios no técnicos, con ayuda contextual en cada campo."

5. **Precisión:**
   > "Todos los valores están redondeados a 2 decimales como especifica el requerimiento."

---

## 🚨 SOLUCIÓN RÁPIDA DE PROBLEMAS

### Si el script no se ejecuta:
```bash
# Opción alternativa
python -m streamlit run app.py
```

### Si faltan dependencias:
```bash
pip install streamlit pandas numpy plotly reportlab
```

### Si el puerto está ocupado:
```bash
streamlit run app.py --server.port 8502
```

### Si no se abre el navegador:
- Ir manualmente a: http://localhost:8501

---

## 📊 DATOS ALTERNATIVOS (Por si el docente no proporciona)

### Para Módulo A:
**Escenario Conservador:**
- Edad: 25, Monto Inicial: $1,000, Aporte: $300 mensual
- 40 años, TEA: 6%

**Escenario Agresivo:**
- Edad: 30, Monto Inicial: $10,000, Aporte: $1,000 mensual
- 30 años, TEA: 10%

### Para Módulo C:
**Bono con Prima:**
- VN: $1,000, Cupón: 8%, Semestral, 5 años, TEA: 6%
- Resultado: VP > VN (Prima)

**Bono con Descuento:**
- VN: $1,000, Cupón: 5%, Semestral, 5 años, TEA: 6%
- Resultado: VP < VN (Descuento)

---

## ⏱️ CRONOMETRAJE SUGERIDO

- **0:00 - 0:30** → Abrir aplicación y mostrar interfaz
- **0:30 - 3:30** → Módulo A completo
- **3:30 - 5:30** → Módulo B completo
- **5:30 - 7:30** → Módulo C completo
- **7:30 - 8:30** → Exportar PDF
- **8:30 - 10:00** → Preguntas y cierre

---

## 💬 DISCURSO DE CIERRE

**Qué decir al finalizar:**

> "En resumen, hemos desarrollado un simulador financiero completo que cumple con todos los requerimientos del proyecto. Implementa los tres módulos solicitados: crecimiento de cartera con interés compuesto, proyección de jubilación con cálculo de pensión e impuestos, y valoración de bonos. El sistema incluye validaciones automáticas, conversión de tasas, gráficas interactivas y exportación a PDF. Todo está diseñado para usuarios no técnicos y está listo para uso profesional. ¿Alguna pregunta?"

---

## ❓ POSIBLES PREGUNTAS Y RESPUESTAS

**P: ¿Cómo se calculan las tasas periódicas?**
R: Usamos la fórmula de tasas equivalentes: i_periodo = (1 + TEA)^(1/n) - 1

**P: ¿Por qué el bono cotiza con descuento?**
R: Porque la tasa de retorno requerida (6%) es mayor a la tasa cupón (5%), haciendo el bono menos atractivo.

**P: ¿Se pueden cambiar los valores después de calcular?**
R: Sí, solo hay que modificar los valores y volver a calcular.

**P: ¿Los datos se guardan?**
R: Los datos permanecen en la sesión, pero para guardar permanentemente hay que exportar a PDF.

**P: ¿Funciona sin internet?**
R: Sí, una vez instalado funciona completamente offline.

---

## ✅ CHECKLIST PRE-DEMOSTRACIÓN

Verificar antes de presentar:

- [ ] Aplicación instalada y probada
- [ ] Python funcionando correctamente
- [ ] Navegador por defecto configurado
- [ ] Datos de prueba preparados
- [ ] Conexión a proyector/pantalla funcionando
- [ ] Backup en USB (por si acaso)
- [ ] Manual de usuario disponible para mostrar
- [ ] Conocer bien el flujo de la demostración

---

## 🎯 CONSEJOS FINALES

1. **Practica antes:** Haz la demostración 2-3 veces antes de la clase
2. **Habla con confianza:** Conoces el proyecto mejor que nadie
3. **Sé conciso:** No te extiendas demasiado en cada módulo
4. **Muestra entusiasmo:** Demuestra que estás orgulloso del trabajo
5. **Prepara un backup:** Ten el proyecto en USB y en la nube
6. **Llega temprano:** Configura todo antes de que llegue el resto
7. **Mantén la calma:** Si algo falla, usa datos alternativos

---

## 📚 DOCUMENTOS DE APOYO

Tener listos para mostrar si es necesario:
- Manual de Usuario (docs/Manual_Usuario.pdf)
- EJEMPLOS.md
- RESUMEN_PROYECTO.md

---

**¡MUCHA SUERTE EN TU PRESENTACIÓN!** 🎓🚀

Recuerda: Este proyecto está completo, profesional y cumple al 100% con los requerimientos. ¡Tú puedes! 💪
