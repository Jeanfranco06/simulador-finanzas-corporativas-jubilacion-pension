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
