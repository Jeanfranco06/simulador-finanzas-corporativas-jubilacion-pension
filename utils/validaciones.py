"""
Módulo de validaciones
Valida las entradas del usuario según los requerimientos del proyecto
"""

from typing import Tuple, Optional


def validar_monto(monto: float, nombre_campo: str = "Monto") -> Tuple[bool, Optional[str]]:
    """
    Valida que un monto sea no negativo
    
    Args:
        monto: Valor a validar
        nombre_campo: Nombre del campo para el mensaje de error
    
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    if monto < 0:
        return False, f"❌ {nombre_campo} no puede ser negativo"
    return True, None


def validar_tea(tea: float) -> Tuple[bool, Optional[str]]:
    """
    Valida que la TEA esté en el rango permitido (0% - 50%)
    
    Args:
        tea: Tasa Efectiva Anual en porcentaje
    
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    if tea < 0 or tea > 50:
        return False, "❌ La TEA debe estar entre 0% y 50%"
    return True, None


def validar_años(años: int, min_años: int = 1) -> Tuple[bool, Optional[str]]:
    """
    Valida que el plazo en años sea válido
    
    Args:
        años: Plazo en años
        min_años: Años mínimos permitidos
    
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    if años < min_años:
        return False, f"❌ El plazo debe ser al menos {min_años} año(s)"
    if años > 100:
        return False, "❌ El plazo no puede exceder 100 años"
    return True, None


def validar_edad(edad_actual: int, edad_retiro: int) -> Tuple[bool, Optional[str]]:
    """
    Valida que las edades sean coherentes
    
    Args:
        edad_actual: Edad actual de la persona
        edad_retiro: Edad de retiro planeada
    
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    if edad_actual < 18:
        return False, "❌ La edad actual debe ser al menos 18 años"
    
    if edad_actual > 100:
        return False, "❌ La edad actual no puede exceder 100 años"
    
    if edad_retiro <= edad_actual:
        return False, "❌ La edad de retiro debe ser mayor a la edad actual"
    
    if edad_retiro > 120:
        return False, "❌ La edad de retiro no puede exceder 120 años"
    
    return True, None


def validar_datos_cartera(
    monto_inicial: float,
    aporte_periodico: float,
    tea: float,
    años: int
) -> Tuple[bool, Optional[str]]:
    """
    Valida todos los datos para la simulación de cartera
    
    Args:
        monto_inicial: Capital inicial
        aporte_periodico: Aporte periódico
        tea: Tasa Efectiva Anual en porcentaje
        años: Plazo en años
    
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    # Validar monto inicial
    es_valido, mensaje = validar_monto(monto_inicial, "Monto inicial")
    if not es_valido:
        return False, mensaje
    
    # Validar aporte periódico
    es_valido, mensaje = validar_monto(aporte_periodico, "Aporte periódico")
    if not es_valido:
        return False, mensaje
    
    # Validar que al menos uno sea mayor a 0
    if monto_inicial == 0 and aporte_periodico == 0:
        return False, "❌ Debe ingresar un monto inicial o un aporte periódico"
    
    # Validar TEA
    es_valido, mensaje = validar_tea(tea)
    if not es_valido:
        return False, mensaje
    
    # Validar años
    es_valido, mensaje = validar_años(años)
    if not es_valido:
        return False, mensaje
    
    return True, None


def validar_datos_bono(
    valor_nominal: float,
    tasa_cupon: float,
    años: int,
    tea_retorno: float
) -> Tuple[bool, Optional[str]]:
    """
    Valida todos los datos para la valoración de bonos
    
    Args:
        valor_nominal: Valor nominal del bono
        tasa_cupon: Tasa cupón anual en porcentaje
        años: Años al vencimiento
        tea_retorno: TEA de retorno esperada
    
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    # Validar valor nominal
    es_valido, mensaje = validar_monto(valor_nominal, "Valor nominal")
    if not es_valido:
        return False, mensaje
    
    if valor_nominal == 0:
        return False, "❌ El valor nominal debe ser mayor a 0"
    
    # Validar tasa cupón
    if tasa_cupon < 0 or tasa_cupon > 50:
        return False, "❌ La tasa cupón debe estar entre 0% y 50%"
    
    # Validar años
    es_valido, mensaje = validar_años(años)
    if not es_valido:
        return False, mensaje
    
    # Validar TEA retorno
    es_valido, mensaje = validar_tea(tea_retorno)
    if not es_valido:
        return False, mensaje
    
    return True, None


def validar_datos_jubilacion(
    edad_actual: int,
    edad_retiro: int,
    años_retiro: int
) -> Tuple[bool, Optional[str]]:
    """
    Valida los datos para la proyección de jubilación
    
    Args:
        edad_actual: Edad actual
        edad_retiro: Edad de retiro
        años_retiro: Años esperados de retiro
    
    Returns:
        Tuple (es_valido, mensaje_error)
    """
    # Validar edades
    es_valido, mensaje = validar_edad(edad_actual, edad_retiro)
    if not es_valido:
        return False, mensaje
    
    # Validar años de retiro
    es_valido, mensaje = validar_años(años_retiro, min_años=1)
    if not es_valido:
        return False, mensaje
    
    if años_retiro > 50:
        return False, "❌ Los años de retiro no pueden exceder 50"
    
    return True, None
