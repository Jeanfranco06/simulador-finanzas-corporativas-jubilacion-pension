from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .forms import CarteraForm, JubilacionForm, BonosForm
from .models import calcular_cartera, calcular_jubilacion, calcular_bonos

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main.route('/cartera', methods=['GET', 'POST'])
def cartera():
    """Módulo A: Crecimiento de Cartera"""
    form = CarteraForm()
    resultado = None

    if form.validate_on_submit():
        # Process form data
        datos = {
            'edad_actual': form.edad_actual.data,
            'monto_inicial': form.monto_inicial.data,
            'aporte_periodico': form.aporte_periodico.data,
            'frecuencia': form.frecuencia.data,
            'tipo_plazo': form.tipo_plazo.data,
            'años': form.años.data if form.tipo_plazo.data == 'años' else None,
            'edad_retiro': form.edad_retiro.data if form.tipo_plazo.data == 'edad' else None,
            'tea': form.tea.data
        }

        try:
            resultado = calcular_cartera(datos)
            # Store results in session for use by other modules (exclude DataFrame)
            session['cartera_resumen'] = resultado['resumen']
            session['cartera_datos'] = datos
        except Exception as e:
            flash(f'Error en el cálculo: {str(e)}', 'error')

    return render_template('cartera.html', form=form, resultado=resultado)

@main.route('/jubilacion', methods=['GET', 'POST'])
def jubilacion():
    """Módulo B: Proyección de Jubilación"""
    form = JubilacionForm()
    resultado = None
    modulo_a_completado = 'cartera_resumen' in session

    if form.validate_on_submit():
        if not modulo_a_completado:
            flash('Debes completar primero el Módulo A (Crecimiento de Cartera)', 'error')
            return redirect(url_for('main.jubilacion'))

        # Process form data
        datos = {
            'tipo_retiro': form.tipo_retiro.data,
            'tipo_impuesto': form.tipo_impuesto.data,
            'años_retiro': form.años_retiro.data if form.tipo_retiro.data == 'pension' else None,
            'tea_retiro': form.tea_retiro.data if form.usar_misma_tea.data == False else None,
            'usar_misma_tea': form.usar_misma_tea.data
        }

        try:
            resultado = calcular_jubilacion(datos)
            # Store results in session
            session['jubilacion_resultado'] = resultado
        except Exception as e:
            flash(f'Error en el cálculo: {str(e)}', 'error')

    return render_template('jubilacion.html', form=form, resultado=resultado, modulo_a_completado=modulo_a_completado)

@main.route('/bonos', methods=['GET', 'POST'])
def bonos():
    """Módulo C: Valoración de Bonos"""
    form = BonosForm()
    resultado = None

    if form.validate_on_submit():
        # Process form data
        datos = {
            'valor_nominal': form.valor_nominal.data,
            'tasa_cupon': form.tasa_cupon.data,
            'frecuencia_pago': form.frecuencia_pago.data,
            'años_bono': form.años_bono.data,
            'tea_retorno': form.tea_retorno.data
        }

        try:
            resultado = calcular_bonos(datos)
        except Exception as e:
            flash(f'Error en el cálculo: {str(e)}', 'error')

    return render_template('bonos.html', form=form, resultado=resultado)

@main.route('/resultado')
def resultado():
    """Mostrar resultados detallados"""
    return render_template('resultado.html')
