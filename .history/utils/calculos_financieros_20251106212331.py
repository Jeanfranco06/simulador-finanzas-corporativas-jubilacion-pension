"""
Módulo de cálculos financieros
Contiene todas las funciones de cálculo para la simulación de jubilación y valoración de bonos
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


def calcular_tasa_periodica(tea: float, frecuencia: str) -> float:
    """
    Convierte la TEA a tasa periódica según la frecuencia
    
    Args:
        tea: Tasa Efectiva Anual (en decimal, ej: 0.08 para 8%)
        frecuencia: 'Mensual', 'Trimestral', 'Semestral', 'Anual'
    
    Returns:
        Tasa periódica equivalente
    """
    periodos_por_año = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }
    
    n = periodos_por_año.get(frecuencia, 12)
    # Fórmula: (1 + TEA)^(1/n) - 1
    tasa_periodica = (1 + tea) ** (1 / n) - 1
    
    return tasa_periodica


def simular_crecimiento_cartera(
    monto_inicial: float,
    aporte_periodico: float,
    tea: float,
    frecuencia: str,
    años: int
) -> pd.DataFrame:
    """
    Simula el crecimiento de una cartera con aportes periódicos
    
    Args:
        monto_inicial: Capital inicial en USD
        aporte_periodico: Aporte periódico en USD
        tea: Tasa Efectiva Anual (en decimal)
        frecuencia: Frecuencia de aportes
        años: Plazo en años
    
    Returns:
        DataFrame con el detalle periodo a periodo
    """
    periodos_por_año = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }
    
    n_periodos_año = periodos_por_año.get(frecuencia, 12)
    total_periodos = años * n_periodos_año
    tasa_periodica = calcular_tasa_periodica(tea, frecuencia)
    
    # Inicializar listas
    periodos = []
    saldos_iniciales = []
    aportes = []
    intereses = []
    saldos_finales = []
    aportes_acumulados = []
    
    saldo = monto_inicial
    aporte_acumulado = monto_inicial
    
    for periodo in range(1, total_periodos + 1):
        saldo_inicial = saldo
        aporte_actual = aporte_periodico
        interes = saldo_inicial * tasa_periodica
        saldo_final = saldo_inicial + aporte_actual + interes
        
        aporte_acumulado += aporte_actual
        
        periodos.append(periodo)
        saldos_iniciales.append(round(saldo_inicial, 2))
        aportes.append(round(aporte_actual, 2))
        intereses.append(round(interes, 2))
        saldos_finales.append(round(saldo_final, 2))
        aportes_acumulados.append(round(aporte_acumulado, 2))
        
        saldo = saldo_final
    
    df = pd.DataFrame({
        'Periodo': periodos,
        'Saldo Inicial (USD)': saldos_iniciales,
        'Aporte (USD)': aportes,
        'Interés Ganado (USD)': intereses,
        'Saldo Final (USD)': saldos_finales,
        'Aportes Acumulados (USD)': aportes_acumulados
    })
    
    return df


def calcular_impuesto(ganancia: float, tipo_impuesto: str) -> float:
    """
    Calcula el impuesto sobre la ganancia
    
    Args:
        ganancia: Ganancia obtenida en USD
        tipo_impuesto: '5% Bolsa Local' o '29.5% Fuente Extranjera'
    
    Returns:
        Monto del impuesto
    """
    tasas_impuesto = {
        '5% Bolsa Local': 0.05,
        '29.5% Fuente Extranjera': 0.295
    }
    
    tasa = tasas_impuesto.get(tipo_impuesto, 0.295)
    return ganancia * tasa


def calcular_pension_mensual(
    capital_disponible: float,
    tea_retiro: float,
    años_retiro: int
) -> float:
    """
    Calcula la pensión mensual estimada durante el retiro
    
    Args:
        capital_disponible: Capital neto disponible después de impuestos
        tea_retiro: Tasa efectiva anual durante el retiro
        años_retiro: Años esperados de retiro
    
    Returns:
        Pensión mensual en USD
    """
    # Convertir TEA a tasa mensual
    tasa_mensual = calcular_tasa_periodica(tea_retiro, 'Mensual')
    n_meses = años_retiro * 12
    
    # Fórmula de anualidad: PMT = PV * [r(1+r)^n] / [(1+r)^n - 1]
    if tasa_mensual == 0:
        pension = capital_disponible / n_meses
    else:
        factor = (1 + tasa_mensual) ** n_meses
        pension = capital_disponible * (tasa_mensual * factor) / (factor - 1)
    
    return pension


def valorar_bono(
    valor_nominal: float,
    tasa_cupon_anual: float,
    frecuencia_pago: str,
    años: int,
    tea_retorno: float
) -> Tuple[pd.DataFrame, float]:
    """
    Valora un bono calculando el valor presente de sus flujos
    
    Args:
        valor_nominal: Valor nominal del bono en USD
        tasa_cupon_anual: Tasa cupón anual (en decimal)
        frecuencia_pago: Frecuencia de pago de cupones
        años: Años al vencimiento
        tea_retorno: Tasa de retorno esperada (TEA en decimal)
    
    Returns:
        Tuple con DataFrame de flujos y valor presente total
    """
    periodos_por_año = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }
    
    n_periodos_año = periodos_por_año.get(frecuencia_pago, 2)
    total_periodos = años * n_periodos_año
    
    # Calcular cupón periódico
    tasa_cupon_periodica = calcular_tasa_periodica(tasa_cupon_anual, frecuencia_pago)
    cupon = valor_nominal * tasa_cupon_periodica
    
    # Calcular tasa de descuento periódica
    tasa_descuento = calcular_tasa_periodica(tea_retorno, frecuencia_pago)
    
    # Calcular flujos
    periodos = []
    flujos = []
    valores_presentes = []
    
    for periodo in range(1, total_periodos + 1):
        # Flujo = cupón, excepto el último periodo que incluye principal
        if periodo == total_periodos:
            flujo = cupon + valor_nominal
        else:
            flujo = cupon
        
        # Valor presente del flujo
        vp = flujo / ((1 + tasa_descuento) ** periodo)
        
        periodos.append(periodo)
        flujos.append(round(flujo, 2))
        valores_presentes.append(round(vp, 2))
    
    df = pd.DataFrame({
        'Periodo': periodos,
        'Flujo (USD)': flujos,
        'Valor Presente (USD)': valores_presentes
    })
    
    valor_presente_total = sum(valores_presentes)
    
    return df, round(valor_presente_total, 2)


def calcular_escenarios_comparativos(
    monto_inicial: float,
    aporte_periodico: float,
    frecuencia: str,
    edad_actual: int,
    edades_retiro: List[int],
    tasas: List[float],
    tipo_impuesto: str,
    años_retiro: int = 25
) -> pd.DataFrame:
    """
    Calcula escenarios comparativos de jubilación
    
    Args:
        monto_inicial: Capital inicial
        aporte_periodico: Aporte periódico
        frecuencia: Frecuencia de aportes
        edad_actual: Edad actual
        edades_retiro: Lista de edades de retiro a comparar
        tasas: Lista de TEAs a comparar
        tipo_impuesto: Tipo de impuesto aplicable
        años_retiro: Años esperados de retiro
    
    Returns:
        DataFrame con comparación de escenarios
    """
    resultados = []
    
    for edad_retiro in edades_retiro:
        años_hasta_retiro = edad_retiro - edad_actual
        
        for tea in tasas:
            # Simular crecimiento
            df_cartera = simular_crecimiento_cartera(
                monto_inicial, aporte_periodico, tea, frecuencia, años_hasta_retiro
            )
            
            capital_acumulado = df_cartera['Saldo Final (USD)'].iloc[-1]
            aportes_totales = df_cartera['Aportes Acumulados (USD)'].iloc[-1]
            ganancia = capital_acumulado - aportes_totales
            impuesto = calcular_impuesto(ganancia, tipo_impuesto)
            capital_neto = capital_acumulado - impuesto
            
            # Calcular pensión
            pension = calcular_pension_mensual(capital_neto, tea, años_retiro)
            
            resultados.append({
                'Edad de Retiro': edad_retiro,
                'TEA (%)': round(tea * 100, 2),
                'Años Ahorrando': años_hasta_retiro,
                'Capital Acumulado (USD)': round(capital_acumulado, 2),
                'Impuesto (USD)': round(impuesto, 2),
                'Capital Neto (USD)': round(capital_neto, 2),
                'Pensión Mensual (USD)': round(pension, 2)
            })
    
    return pd.DataFrame(resultados)


def simular_cartera_con_inflacion(
    monto_inicial: float,
    aporte_inicial: float,
    tea: float,
    frecuencia: str,
    años: int,
    tasa_inflacion: float,
    escalado_aportes: float = 0.0,
    reajuste_jubilacion: bool = False,
    años_retiro: int = 25
) -> Tuple[pd.DataFrame, Dict]:
    """
    Simula crecimiento de cartera con ajustes automáticos por inflación

    Args:
        monto_inicial: Capital inicial en USD
        aporte_inicial: Aporte inicial periódico en USD
        tea: Tasa Efectiva Anual (en decimal)
        frecuencia: Frecuencia de aportes
        años: Plazo en años
        tasa_inflacion: Tasa de inflación anual (en decimal)
        escalado_aportes: Incremento anual de aportes por inflación (en decimal)
        reajuste_jubilacion: Si aplicar reajuste por costo de vida en jubilación
        años_retiro: Años esperados de retiro

    Returns:
        Tuple con DataFrame detallado y resumen
    """
    periodos_por_año = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }

    n_periodos_año = periodos_por_año.get(frecuencia, 12)
    total_periodos = años * n_periodos_año
    tasa_periodica = calcular_tasa_periodica(tea, frecuencia)
    inflacion_periodica = calcular_tasa_periodica(tasa_inflacion, frecuencia)

    # Inicializar listas
    periodos = []
    saldos_iniciales = []
    aportes = []
    intereses = []
    saldos_finales = []
    aportes_acumulados = []
    inflacion_acumulada = []

    saldo = monto_inicial
    aporte_actual = aporte_inicial
    aporte_acumulado = monto_inicial
    inflacion_acum = 0

    for periodo in range(1, total_periodos + 1):
        saldo_inicial = saldo

        # Calcular aporte ajustado por escalado automático
        if periodo > 1 and periodo % n_periodos_año == 1:  # Nuevo año
            aporte_actual *= (1 + escalado_aportes)

        aporte_actual_periodo = aporte_actual

        # Calcular interés real (descontando inflación)
        interes_nominal = saldo_inicial * tasa_periodica
        interes_real = interes_nominal / (1 + inflacion_periodica) - saldo_inicial * inflacion_periodica

        saldo_final = saldo_inicial + aporte_actual_periodo + interes_real

        aporte_acumulado += aporte_actual_periodo
        inflacion_acum += saldo_inicial * inflacion_periodica

        periodos.append(periodo)
        saldos_iniciales.append(round(saldo_inicial, 2))
        aportes.append(round(aporte_actual_periodo, 2))
        intereses.append(round(interes_real, 2))
        saldos_finales.append(round(saldo_final, 2))
        aportes_acumulados.append(round(aporte_acumulado, 2))
        inflacion_acumulada.append(round(inflacion_acum, 2))

        saldo = saldo_final

    df = pd.DataFrame({
        'Periodo': periodos,
        'Saldo Inicial (USD)': saldos_iniciales,
        'Aporte (USD)': aportes,
        'Interés Real (USD)': intereses,
        'Saldo Final (USD)': saldos_finales,
        'Aportes Acumulados (USD)': aportes_acumulados,
        'Inflación Acumulada (USD)': inflacion_acumulada
    })

    # Calcular resumen
    capital_final = df['Saldo Final (USD)'].iloc[-1]
    aportes_totales = df['Aportes Acumulados (USD)'].iloc[-1]
    ganancia_bruta = capital_final - aportes_totales
    inflacion_total = df['Inflación Acumulada (USD)'].iloc[-1]
    ganancia_real = ganancia_bruta - inflacion_total

    # Calcular pensión ajustada por costo de vida si aplica
    pension_mensual = None
    if reajuste_jubilacion:
        # Calcular pensión inicial
        pension_inicial = calcular_pension_mensual(capital_final, tea, años_retiro)
        # Aplicar reajuste por costo de vida (aproximadamente)
        pension_mensual = pension_inicial * (1 + tasa_inflacion) ** (años_retiro / 2)  # Promedio durante retiro

    resumen = {
        'capital_final': round(capital_final, 2),
        'aportes_totales': round(aportes_totales, 2),
        'ganancia_bruta': round(ganancia_bruta, 2),
        'inflacion_total': round(inflacion_total, 2),
        'ganancia_real': round(ganancia_real, 2),
        'rentabilidad_real': round((ganancia_real / aportes_totales) * 100, 2) if aportes_totales > 0 else 0,
        'pension_mensual_ajustada': round(pension_mensual, 2) if pension_mensual else None,
        'tasa_inflacion': round(tasa_inflacion * 100, 2),
        'escalado_aportes': round(escalado_aportes * 100, 2)
    }

    return df, resumen


def comparar_estrategias_inversion(
    monto_inicial: float,
    aporte_periodico: float,
    frecuencia: str,
    años: int,
    estrategias: List[Dict]
) -> pd.DataFrame:
    """
    Compara diferentes estrategias de inversión

    Args:
        monto_inicial: Capital inicial
        aporte_periodico: Aporte periódico
        frecuencia: Frecuencia de aportes
        años: Plazo en años
        estrategias: Lista de estrategias con sus parámetros

    Returns:
        DataFrame con comparación de estrategias
    """
    resultados = []

    for estrategia in estrategias:
        nombre = estrategia['nombre']
        tea = estrategia['tea']
        volatilidad = estrategia.get('volatilidad', 0)
        rebalanceo = estrategia.get('rebalanceo', False)

        # Simular múltiples escenarios con volatilidad
        simulaciones = []
        for i in range(50):  # 50 simulaciones por estrategia
            # Aplicar volatilidad aleatoria
            tea_ajustada = tea * (1 + np.random.normal(0, volatilidad))

            try:
                df = simular_crecimiento_cartera(
                    monto_inicial, aporte_periodico, tea_ajustada, frecuencia, años
                )
                capital_final = df['Saldo Final (USD)'].iloc[-1]
                simulaciones.append(capital_final)
            except:
                continue

        if simulaciones:
            capital_promedio = np.mean(simulaciones)
            capital_min = np.min(simulaciones)
            capital_max = np.max(simulaciones)
            volatilidad_real = np.std(simulaciones) / capital_promedio if capital_promedio > 0 else 0

            # Calcular métricas de Sharpe simplificado (retorno / volatilidad)
            sharpe_ratio = (capital_promedio - monto_inicial) / np.std(simulaciones) if np.std(simulaciones) > 0 else 0

            resultados.append({
                'Estrategia': nombre,
                'Capital Promedio (USD)': round(capital_promedio, 2),
                'Capital Mínimo (USD)': round(capital_min, 2),
                'Capital Máximo (USD)': round(capital_max, 2),
                'Volatilidad (%)': round(volatilidad_real * 100, 2),
                'TEA Esperada (%)': round(tea * 100, 2),
                'Ratio Sharpe': round(sharpe_ratio, 3),
                'Probabilidad Éxito (%)': round((len([x for x in simulaciones if x > capital_promedio * 0.8]) / len(simulaciones)) * 100, 1)
            })

    return pd.DataFrame(resultados)


def calcular_benchmarking(
    estrategia_personal: Dict,
    benchmarks: List[Dict],
    monto_inicial: float,
    aporte_periodico: float,
    frecuencia: str,
    años: int
) -> pd.DataFrame:
    """
    Compara estrategia personal vs benchmarks del mercado

    Args:
        estrategia_personal: Parámetros de la estrategia personal
        benchmarks: Lista de benchmarks (ej: S&P 500, Bonos, etc.)
        monto_inicial: Capital inicial
        aporte_periodico: Aporte periódico
        frecuencia: Frecuencia de aportes
        años: Plazo en años

    Returns:
        DataFrame con comparación vs benchmarks
    """
    resultados = []

    # Calcular estrategia personal - usar la misma TEA pero con validación
    tea_personal = min(estrategia_personal['tea'], 0.50)  # Limitar TEA al 50% máximo para evitar números astronómicos
    df_personal = simular_crecimiento_cartera(
        monto_inicial, aporte_periodico, tea_personal,
        frecuencia, años
    )
    capital_personal = df_personal['Saldo Final (USD)'].iloc[-1]

    resultados.append({
        'Benchmark': 'Tu Estrategia',
        'Capital Final (USD)': round(capital_personal, 2),
        'TEA (%)': round(estrategia_personal['tea'] * 100, 2),
        'Diferencia vs Mercado (%)': 0,
        'Rendimiento Anualizado (%)': round(estrategia_personal['tea'] * 100, 2)
    })

    # Calcular benchmarks
    for benchmark in benchmarks:
        df_benchmark = simular_crecimiento_cartera(
            monto_inicial, aporte_periodico, benchmark['tea'],
            frecuencia, años
        )
        capital_benchmark = df_benchmark['Saldo Final (USD)'].iloc[-1]

        # Evitar división por cero o números muy pequeños
        if capital_benchmark > 0:
            diferencia = ((capital_personal - capital_benchmark) / capital_benchmark) * 100
        else:
            diferencia = 0  # Si el benchmark da 0, no hay diferencia calculable

        resultados.append({
            'Benchmark': benchmark['nombre'],
            'Capital Final (USD)': round(capital_benchmark, 2),
            'TEA (%)': round(benchmark['tea'] * 100, 2),
            'Diferencia vs Mercado (%)': round(diferencia, 2),
            'Rendimiento Anualizado (%)': round(benchmark['tea'] * 100, 2)
        })

    return pd.DataFrame(resultados)


def simular_rebalanceo_automatico(
    monto_inicial: float,
    aporte_periodico: float,
    frecuencia: str,
    años: int,
    activos: List[Dict],
    frecuencia_rebalanceo: str = 'Anual'
) -> Tuple[pd.DataFrame, Dict]:
    """
    Simula estrategia con rebalanceo automático de portafolio

    Args:
        monto_inicial: Capital inicial
        aporte_periodico: Aporte periódico
        frecuencia: Frecuencia de aportes
        años: Plazo en años
        activos: Lista de activos con sus pesos y TEAs
        frecuencia_rebalanceo: Frecuencia de rebalanceo ('Mensual', 'Trimestral', 'Anual')

    Returns:
        Tuple con DataFrame detallado y resumen
    """
    periodos_por_año = {
        'Mensual': 12,
        'Trimestral': 4,
        'Anual': 1
    }

    n_periodos_año = periodos_por_año.get(frecuencia, 12)
    n_rebalanceo = periodos_por_año.get(frecuencia_rebalanceo, 1)
    total_periodos = años * n_periodos_año

    # Inicializar portafolio
    portafolio = {}
    total_inicial = monto_inicial

    for activo in activos:
        portafolio[activo['nombre']] = {
            'peso_objetivo': activo['peso'],
            'monto': monto_inicial * activo['peso'],
            'tea': activo['tea']
        }

    # Simular periodo a periodo
    periodos = []
    saldos_totales = []
    saldos_por_activo = {activo['nombre']: [] for activo in activos}

    saldo_total = monto_inicial

    for periodo in range(1, total_periodos + 1):
        # Aplicar aportes y crecimiento
        aporte_actual = aporte_periodico

        # Rebalancear si corresponde
        if periodo % n_rebalanceo == 1:
            total_actual = sum(activo['monto'] for activo in portafolio.values())
            for activo in portafolio.values():
                activo['monto'] = total_actual * activo['peso_objetivo']

        # Aplicar crecimiento a cada activo
        for activo in portafolio.values():
            tasa_periodica = calcular_tasa_periodica(activo['tea'], frecuencia)
            activo['monto'] *= (1 + tasa_periodica)

        # Agregar aporte proporcionalmente
        total_actual = sum(activo['monto'] for activo in portafolio.values())
        for activo in portafolio.values():
            peso_actual = activo['monto'] / total_actual if total_actual > 0 else activo['peso_objetivo']
            activo['monto'] += aporte_actual * peso_actual

        # Calcular total
        saldo_total = sum(activo['monto'] for activo in portafolio.values())

        # Registrar datos
        periodos.append(periodo)
        saldos_totales.append(round(saldo_total, 2))
        for activo in activos:
            saldos_por_activo[activo['nombre']].append(round(portafolio[activo['nombre']]['monto'], 2))

    # Crear DataFrame
    data = {'Periodo': periodos, 'Saldo Total (USD)': saldos_totales}
    data.update(saldos_por_activo)
    df = pd.DataFrame(data)

    # Calcular resumen
    capital_final = df['Saldo Total (USD)'].iloc[-1]
    aportes_totales = monto_inicial + (aporte_periodico * total_periodos)
    ganancia_total = capital_final - aportes_totales

    resumen = {
        'capital_final': round(capital_final, 2),
        'aportes_totales': round(aportes_totales, 2),
        'ganancia_total': round(ganancia_total, 2),
        'rentabilidad_total': round((ganancia_total / aportes_totales) * 100, 2) if aportes_totales > 0 else 0,
        'frecuencia_rebalanceo': frecuencia_rebalanceo,
        'numero_activos': len(activos)
    }

    return df, resumen
