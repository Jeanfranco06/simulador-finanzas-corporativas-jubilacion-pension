"""
Financial calculation models for the simulator
"""
import pandas as pd
import numpy as np
from datetime import datetime

def calcular_cartera(datos):
    """
    Calculate portfolio growth (Módulo A)

    Args:
        datos: Dictionary with form data

    Returns:
        Dictionary with calculation results
    """
    # Extract data
    edad_actual = datos['edad_actual']
    monto_inicial = datos['monto_inicial']
    aporte_periodico = datos['aporte_periodico'] or 0
    frecuencia = datos['frecuencia']
    tea = datos['tea'] / 100  # Convert to decimal

    # Calculate years
    if datos['tipo_plazo'] == 'años':
        años = datos['años']
        edad_retiro = edad_actual + años
    else:
        edad_retiro = datos['edad_retiro']
        años = edad_retiro - edad_actual

    # Calculate periods per year
    periodos_por_año = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }

    periodos_año = periodos_por_año[frecuencia]
    total_periodos = años * periodos_año

    # Calculate periodic rate
    tasa_periodica = (1 + tea) ** (1 / periodos_año) - 1

    # Initialize variables
    saldo = monto_inicial
    aportes_acumulados = monto_inicial
    resultados = []

    # Calculate growth period by period
    for periodo in range(1, total_periodos + 1):
        # Add periodic contribution (except first period for initial amount)
        if periodo > 1:
            saldo += aporte_periodico
            aportes_acumulados += aporte_periodico

        # Apply interest
        interes = saldo * tasa_periodica
        saldo += interes

        # Record results
        resultados.append({
            'Periodo': periodo,
            'Saldo Inicial': saldo - interes - (aporte_periodico if periodo > 1 else 0),
            'Aportes': aporte_periodico if periodo > 1 else 0,
            'Interés': interes,
            'Saldo Final': saldo,
            'Aportes Acumulados': aportes_acumulados
        })

    # Create DataFrame
    df = pd.DataFrame(resultados)

    # Calculate summary
    capital_final = df['Saldo Final'].iloc[-1]
    aportes_totales = df['Aportes Acumulados'].iloc[-1]
    ganancia_bruta = capital_final - aportes_totales
    rentabilidad = (ganancia_bruta / aportes_totales * 100) if aportes_totales > 0 else 0

    return {
        'dataframe': df,
        'resumen': {
            'capital_final': capital_final,
            'aportes_totales': aportes_totales,
            'ganancia_bruta': ganancia_bruta,
            'rentabilidad': rentabilidad,
            'edad_retiro': edad_retiro,
            'años': años,
            'frecuencia': frecuencia
        }
    }

def calcular_jubilacion(datos):
    """
    Calculate retirement projection (Módulo B)

    Args:
        datos: Dictionary with form data

    Returns:
        Dictionary with calculation results
    """
    # This would need the portfolio data from session/module A
    # For now, return placeholder
    return {
        'tipo_retiro': datos['tipo_retiro'],
        'tipo_impuesto': datos['tipo_impuesto'],
        'mensaje': 'Este módulo requiere datos del Módulo A primero'
    }

def calcular_bonos(datos):
    """
    Calculate bond valuation (Módulo C)

    Args:
        datos: Dictionary with form data

    Returns:
        Dictionary with calculation results
    """
    # Extract data
    valor_nominal = datos['valor_nominal']
    tasa_cupon = datos['tasa_cupon'] / 100  # Convert to decimal
    frecuencia_pago = datos['frecuencia_pago']
    años = datos['años_bono']
    tea_retorno = datos['tea_retorno'] / 100  # Convert to decimal

    # Calculate periods per year
    periodos_por_año = {
        'Mensual': 12,
        'Bimestral': 6,
        'Trimestral': 4,
        'Cuatrimestral': 3,
        'Semestral': 2,
        'Anual': 1
    }

    periodos_año = periodos_por_año[frecuencia_pago]
    total_periodos = años * periodos_año

    # Calculate periodic rates
    cupon_periodico = valor_nominal * tasa_cupon / periodos_año
    tasa_descuento_periodica = (1 + tea_retorno) ** (1 / periodos_año) - 1

    # Calculate cash flows
    flujos = []
    valor_presente_total = 0

    for periodo in range(1, total_periodos + 1):
        # Determine if it's the last period (includes face value)
        if periodo == total_periodos:
            flujo_nominal = cupon_periodico + valor_nominal
        else:
            flujo_nominal = cupon_periodico

        # Calculate present value
        valor_presente = flujo_nominal / ((1 + tasa_descuento_periodica) ** periodo)
        valor_presente_total += valor_presente

        flujos.append({
            'Periodo': periodo,
            'Flujo (USD)': flujo_nominal,
            'Valor Presente (USD)': valor_presente
        })

    # Create DataFrame
    df = pd.DataFrame(flujos)

    # Determine if premium, discount, or par
    if valor_presente_total > valor_nominal:
        estado = 'Prima'
    elif valor_presente_total < valor_nominal:
        estado = 'Descuento'
    else:
        estado = 'Par'

    return {
        'dataframe': df,
        'resumen': {
            'valor_presente_total': valor_presente_total,
            'valor_nominal': valor_nominal,
            'diferencia': valor_presente_total - valor_nominal,
            'estado': estado,
            'tasa_cupon': tasa_cupon * 100,
            'tea_retorno': tea_retorno * 100
        }
    }
