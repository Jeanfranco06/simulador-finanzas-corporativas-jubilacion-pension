# EJEMPLOS DE USO
## Simulador Financiero de Jubilación

Este archivo contiene ejemplos prácticos para probar cada módulo del simulador.

---

## 📊 MÓDULO A: CRECIMIENTO DE CARTERA

### Ejemplo 1: Ahorro Mensual Conservador
**Escenario:** Persona joven comenzando a ahorrar

**Datos de entrada:**
- Edad Actual: 25 años
- Monto Inicial: $1,000 USD
- Aporte Periódico: $300 USD
- Frecuencia: Mensual
- Edad de Jubilación: 65 años (40 años de ahorro)
- TEA: 6%

**Resultado esperado:**
- Capital Final: ~$603,000 USD
- Ganancia significativa por el interés compuesto
- Gráfica mostrando crecimiento exponencial

---

### Ejemplo 2: Ahorro Agresivo con Alta Rentabilidad
**Escenario:** Persona con capacidad de ahorro elevada

**Datos de entrada:**
- Edad Actual: 30 años
- Monto Inicial: $10,000 USD
- Aporte Periódico: $1,000 USD
- Frecuencia: Mensual
- Edad de Jubilación: 60 años (30 años de ahorro)
- TEA: 10%

**Resultado esperado:**
- Capital Final: ~$2,300,000 USD
- Alta rentabilidad por tasa agresiva
- Comparación clara entre aportes y ganancias

---

### Ejemplo 3: Ahorro Semestral Moderado
**Escenario:** Persona con ingresos variables

**Datos de entrada:**
- Edad Actual: 35 años
- Monto Inicial: $5,000 USD
- Aporte Periódico: $3,000 USD
- Frecuencia: Semestral
- Años: 25 años
- TEA: 8%

**Resultado esperado:**
- Capital Final: ~$284,000 USD
- Menos periodos pero aportes mayores
- Crecimiento sostenido

---

## 🏦 MÓDULO B: PROYECCIÓN DE JUBILACIÓN

### Ejemplo 1: Pensión Mensual con Impuesto Local
**Escenario:** Jubilación con inversiones en bolsa local

**Datos previos (del Módulo A):**
- Capital Acumulado: $500,000 USD
- Aportes Totales: $200,000 USD
- Ganancia: $300,000 USD

**Datos de entrada:**
- Tipo de Retiro: Pensión Mensual
- Tipo de Impuesto: 5% Bolsa Local
- Años Esperados de Retiro: 25 años
- TEA durante retiro: 5%

**Resultado esperado:**
- Impuesto: $15,000 USD (5% de $300,000)
- Capital Neto: $485,000 USD
- Pensión Mensual: ~$2,830 USD/mes

---

### Ejemplo 2: Cobro Total con Impuesto Extranjero
**Escenario:** Retiro único de inversiones extranjeras

**Datos previos:**
- Capital Acumulado: $1,000,000 USD
- Aportes Totales: $400,000 USD
- Ganancia: $600,000 USD

**Datos de entrada:**
- Tipo de Retiro: Cobro Total
- Tipo de Impuesto: 29.5% Fuente Extranjera

**Resultado esperado:**
- Impuesto: $177,000 USD (29.5% de $600,000)
- Capital Neto: $823,000 USD
- Pago único total

---

### Ejemplo 3: Comparación de Escenarios
**Escenario:** Evaluar diferentes edades de retiro

**Datos para comparar:**
- Edades de retiro: 60, 65, 70 años
- TEAs: 6%, 8%, 10%
- Permite ver cómo cambia la pensión según decisiones

---

## 💵 MÓDULO C: VALORACIÓN DE BONOS

### Ejemplo 1: Bono Corporativo a 5 Años
**Escenario:** Valorar un bono corporativo típico

**Datos de entrada:**
- Valor Nominal: $1,000 USD
- Tasa Cupón Anual: 5%
- Frecuencia de Pago: Semestral
- Plazo: 5 años
- TEA Retorno Esperada: 6%

**Resultado esperado:**
- Valor Presente: ~$957.35 USD
- Cotiza con DESCUENTO
- La tasa de mercado (6%) es mayor al cupón (5%)

---

### Ejemplo 2: Bono con Prima
**Escenario:** Bono atractivo que paga más que el mercado

**Datos de entrada:**
- Valor Nominal: $1,000 USD
- Tasa Cupón Anual: 8%
- Frecuencia de Pago: Trimestral
- Plazo: 10 años
- TEA Retorno Esperada: 6%

**Resultado esperado:**
- Valor Presente: ~$1,149 USD
- Cotiza con PRIMA
- El cupón (8%) es mayor a la tasa de mercado (6%)

---

### Ejemplo 3: Bono Gubernamental
**Escenario:** Bono de bajo riesgo a largo plazo

**Datos de entrada:**
- Valor Nominal: $10,000 USD
- Tasa Cupón Anual: 3%
- Frecuencia de Pago: Anual
- Plazo: 20 años
- TEA Retorno Esperada: 3%

**Resultado esperado:**
- Valor Presente: $10,000 USD
- Cotiza A LA PAR
- Tasa cupón = Tasa requerida

---

## 🎯 CASO COMPLETO: PLANIFICACIÓN INTEGRAL

### Perfil: María, 28 años, Ingeniera de Sistemas

**Situación Actual:**
- Edad: 28 años
- Capital inicial: $5,000 USD (ahorros actuales)
- Capacidad de ahorro: $500 USD mensuales
- Edad objetivo de jubilación: 65 años
- Proyección de retiro: 30 años

### PASO 1: Módulo A - Simular Crecimiento
**Datos:**
- Monto Inicial: $5,000 USD
- Aporte Periódico: $500 USD
- Frecuencia: Mensual
- Años: 37 años (65 - 28)
- TEA: 8% (rentabilidad histórica moderada)

**Resultado:**
- Capital Final: ~$1,153,000 USD
- Aportes Totales: $227,000 USD
- Ganancia: ~$926,000 USD

### PASO 2: Módulo B - Calcular Pensión
**Datos:**
- Capital Acumulado: $1,153,000 USD
- Tipo de Retiro: Pensión Mensual
- Impuesto: 29.5% Fuente Extranjera
- Años de Retiro: 30 años
- TEA Retiro: 5%

**Resultado:**
- Impuesto: $273,170 USD (29.5% de $926,000)
- Capital Neto: $879,830 USD
- Pensión Mensual: ~$5,144 USD/mes

### PASO 3: Análisis de Bonos (Opcional)
**Escenario:** María quiere invertir parte de sus ahorros en bonos

**Bono analizado:**
- Valor Nominal: $1,000 USD
- Tasa Cupón: 6%
- Frecuencia: Semestral
- Plazo: 10 años
- TEA Esperada: 7%

**Resultado:**
- Valor Presente: ~$929 USD
- Puede comprar con descuento

### CONCLUSIÓN:
María puede:
1. Jubilarse a los 65 años
2. Recibir ~$5,144 USD mensuales
3. Mantener su nivel de vida durante 30 años
4. Complementar con inversiones en bonos

---

## 💡 CONSEJOS PARA USAR LOS EJEMPLOS

1. **Comience con ejemplos simples:** Use el Ejemplo 1 de cada módulo primero
2. **Experimente con variables:** Cambie las tasas y vea cómo afecta los resultados
3. **Compare escenarios:** Use el comparador del Módulo B para evaluar opciones
4. **Documente sus cálculos:** Exporte cada simulación importante a PDF
5. **Revise periódicamente:** Actualice sus proyecciones cada año

---

## 📝 NOTAS IMPORTANTES

- **Los resultados son proyecciones:** No garantías de rendimiento futuro
- **Considere inflación:** Los valores son nominales, no ajustados por inflación
- **Diversifique:** No ponga todos sus ahorros en una sola inversión
- **Consulte profesionales:** Para decisiones importantes, consulte un asesor financiero
- **Actualice regularmente:** Revise y ajuste su plan cada 6-12 meses

---

## 🔄 EJERCICIOS PROPUESTOS

### Ejercicio 1: Efecto del Tiempo
Compare dos escenarios con el mismo aporte mensual ($500) pero diferentes plazos:
- Escenario A: 20 años
- Escenario B: 40 años
**Pregunta:** ¿Cuánto más acumula por duplicar el plazo?

### Ejercicio 2: Impacto de la Tasa
Manteniendo todo igual, compare TEAs de:
- 5%, 8%, 12%
**Pregunta:** ¿Cuál es el efecto de 1% adicional de rentabilidad?

### Ejercicio 3: Frecuencia de Aportes
Compare el mismo aporte anual distribuido:
- Mensual ($100 x 12)
- Trimestral ($300 x 4)
- Anual ($1,200 x 1)
**Pregunta:** ¿Cuál estrategia acumula más?

### Ejercicio 4: Decisión de Jubilación
Compare jubilarse a 60, 65 y 70 años
**Pregunta:** ¿Vale la pena trabajar 5 años más?

---

**¡Feliz planificación financiera!**

Para más información, consulte el Manual de Usuario en `docs/Manual_Usuario.pdf`
