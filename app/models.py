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
        datos: Dictionary with form data and portfolio data from session

    Returns:
        Dictionary with calculation results
    """
    from flask import session

    # Get portfolio data from session
    resumen_cartera = session.get('cartera_resumen')
    cartera_datos = session.get('cartera_datos')

    if not resumen_cartera or not cartera_datos:
        return {
            'tipo_retiro': datos['tipo_retiro'],
            'tipo_impuesto': datos['tipo_impuesto'],
            'mensaje': 'Este módulo requiere datos del Módulo A primero'
        }

    # Extract portfolio summary
    capital_final = resumen_cartera['capital_final']
    tea_cartera = cartera_datos['tea'] / 100  # Convert back to decimal

    # Extract retirement parameters
    tipo_retiro = datos['tipo_retiro']
    tipo_impuesto = datos['tipo_impuesto']
    años_retiro = datos.get('años_retiro', 25)  # Default 25 years if not specified
    usar_misma_tea = datos.get('usar_misma_tea', True)
    tea_retiro = datos.get('tea_retiro', tea_cartera * 100) / 100 if not usar_misma_tea else tea_cartera

    # Calculate monthly pension based on retirement type
    if tipo_retiro == 'pension':
        # Calculate monthly pension that lasts for the specified years
        # Using annuity formula: PMT = PV / [(1 - (1+r)^-n)/r]
        r_mensual = tea_retiro / 12
        n_meses = años_retiro * 12

        if r_mensual == 0:
            pension_mensual = capital_final / n_meses
        else:
            pension_mensual = capital_final * (r_mensual * (1 + r_mensual)**n_meses) / ((1 + r_mensual)**n_meses - 1)
    else:
        # Lump sum withdrawal
        pension_mensual = capital_final  # One-time payment

    # Calculate taxes based on form choices
    if tipo_impuesto == '29.5':
        tasa_impuesto = 0.295  # 29.5% tax
        impuesto_mensual = pension_mensual * tasa_impuesto
        pension_neta_mensual = pension_mensual - impuesto_mensual
    elif tipo_impuesto == '5':
        tasa_impuesto = 0.05  # 5% tax
        impuesto_mensual = pension_mensual * tasa_impuesto
        pension_neta_mensual = pension_mensual - impuesto_mensual
    else:
        # Default to no tax if unknown type
        impuesto_mensual = 0
        pension_neta_mensual = pension_mensual

    # Calculate annual amounts
    pension_anual = pension_mensual * 12
    impuesto_anual = impuesto_mensual * 12
    pension_neta_anual = pension_neta_mensual * 12

    # Calculate total withdrawal over retirement period
    if tipo_retiro == 'pension':
        retiro_total = pension_mensual * 12 * años_retiro
    else:
        retiro_total = capital_final

    return {
        'tipo_retiro': tipo_retiro,
        'tipo_impuesto': tipo_impuesto,
        'capital_inicial': capital_final,
        'pension_mensual_bruta': pension_mensual,
        'impuesto_mensual': impuesto_mensual,
        'pension_mensual_neta': pension_neta_mensual,
        'pension_anual_bruta': pension_anual,
        'impuesto_anual': impuesto_anual,
        'pension_anual_neta': pension_neta_anual,
        'años_retiro': años_retiro,
        'retiro_total': retiro_total,
        'tea_retiro': tea_retiro * 100,
        'mensaje': 'Cálculo de jubilación completado exitosamente'
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
