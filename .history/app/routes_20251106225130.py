from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, send_file, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .forms import CarteraForm, JubilacionForm, BonosForm
from .models import (
    db, User, Simulation, Template, Achievement, UserAchievement,
    calcular_cartera, calcular_jubilacion, calcular_bonos,
    get_or_create_user, update_user_stats, check_achievements
)
from utils.pdf_generator import generar_pdf_cartera, generar_pdf_bono, generar_pdf_jubilacion, generar_pdf_comparacion
from utils.manual_usuario import crear_manual_usuario
from utils.calculos_financieros import (
    simular_cartera_con_inflacion,
    comparar_estrategias_inversion,
    calcular_benchmarking,
    simular_rebalanceo_automatico
)
from datetime import datetime
import numpy as np
import uuid

main = Blueprint('main', __name__)

def is_ajax_request():
    """Check if the request is an AJAX request"""
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

def generate_cartera_table_html(dataframe):
    """Generate properly formatted HTML table for cartera results"""
    html = '''
    <table class="min-w-full divide-y divide-secondary-200">
        <thead class="bg-secondary-100 sticky top-0">
            <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Periodo</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Saldo Inicial</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Aportes</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Interés</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Saldo Final</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Aportes Acumulados</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-secondary-200">
    '''

    for _, row in dataframe.iterrows():
        html += f'''
            <tr class="hover:bg-secondary-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-secondary-900">{int(row['Periodo'])}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">${row['Saldo Inicial']:.2f}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">${row['Aportes']:.2f}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">${row['Interés']:.2f}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-primary-600">${row['Saldo Final']:.2f}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">${row['Aportes Acumulados']:.2f}</td>
            </tr>
        '''

    html += '''
        </tbody>
    </table>
    '''

    return html

def generate_cartera_summary_html(dataframe):
    """Generate summary view HTML for cartera results"""
    total_rows = len(dataframe)
    if total_rows == 0:
        return ""

    # Get key periods: start, middle, end
    periods_to_show = []
    if total_rows >= 3:
        periods_to_show = [0, total_rows // 2, total_rows - 1]  # First, middle, last
    else:
        periods_to_show = list(range(total_rows))  # Show all if less than 3

    html = '<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">'

    period_names = ['Inicio', 'Mitad del Periodo', 'Final']
    period_labels = ['Periodo 1', f'Periodo {(total_rows // 2) + 1}', f'Periodo {total_rows}']

    for i, period_idx in enumerate(periods_to_show):
        if period_idx < total_rows:
            row = dataframe.iloc[period_idx]
            html += f'''
                <div class="bg-gradient-to-br from-primary-50 to-primary-100 p-6 rounded-xl border border-primary-200">
                    <div class="flex items-center mb-4">
                        <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center mr-3">
                            <i class="fas fa-{"play" if i == 0 else "chart-line" if i == 1 else "trophy"} text-primary-600"></i>
                        </div>
                        <div>
                            <h4 class="font-semibold text-primary-900">{period_names[i]}</h4>
                            <p class="text-sm text-primary-700">{period_labels[i]}</p>
                        </div>
                    </div>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-primary-700">Capital:</span>
                            <span class="font-semibold">${row['Saldo Final']:.2f}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-primary-700">Aportes:</span>
                            <span class="font-semibold">${row['Aportes Acumulados']:.2f}</span>
                        </div>
                    </div>
                </div>
            '''

    html += '</div>'

    # Add key milestones table
    html += '''
        <div class="bg-secondary-50 rounded-xl p-6">
            <h4 class="text-lg font-semibold text-secondary-900 mb-4 flex items-center">
                <i class="fas fa-calendar-check text-primary-600 mr-2"></i>
                Hitos Principales
            </h4>
            <div class="overflow-x-auto">
                <table class="min-w-full">
                    <thead>
                        <tr class="border-b border-secondary-200">
                            <th class="px-4 py-3 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Periodo</th>
                            <th class="px-4 py-3 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Capital</th>
                            <th class="px-4 py-3 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Aportes</th>
                            <th class="px-4 py-3 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Interés</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-secondary-200">
    '''

    # Show key periods (every 4th period or so)
    step = max(1, (total_rows - 1) // 4)
    for i in range(0, total_rows, step):
        if i < total_rows:
            row = dataframe.iloc[i]
            html += f'''
                <tr class="hover:bg-white transition-colors">
                    <td class="px-4 py-3 text-sm font-medium text-secondary-900">{int(row['Periodo'])}</td>
                    <td class="px-4 py-3 text-sm font-bold text-primary-600">${row['Saldo Final']:.2f}</td>
                    <td class="px-4 py-3 text-sm text-secondary-700">${row['Aportes Acumulados']:.2f}</td>
                    <td class="px-4 py-3 text-sm text-green-600 font-medium">${row['Interés']:.2f}</td>
                </tr>
            '''

    # Always show the final period
    if total_rows > 1:
        last_row = dataframe.iloc[-1]
        html += f'''
            <tr class="hover:bg-white transition-colors bg-primary-50">
                <td class="px-4 py-3 text-sm font-bold text-primary-900">{int(last_row['Periodo'])}</td>
                <td class="px-4 py-3 text-sm font-bold text-primary-600">${last_row['Saldo Final']:.2f}</td>
                <td class="px-4 py-3 text-sm font-bold text-primary-900">${last_row['Aportes Acumulados']:.2f}</td>
                <td class="px-4 py-3 text-sm font-bold text-green-600">${last_row['Interés']:.2f}</td>
            </tr>
        '''

    html += '''
                    </tbody>
                </table>
            </div>
            <div class="mt-4 text-center">
                <p class="text-sm text-secondary-600">
                    <i class="fas fa-info-circle mr-1"></i>
    '''

    if total_rows <= 5:
        html += f'Mostrando {total_rows} periodos clave de {total_rows} totales'
    else:
        html += f'Mostrando 5 periodos clave de {total_rows} totales'

    html += '''
                </p>
            </div>
        </div>
    '''

    return html

def generate_bonos_table_html(dataframe):
    """Generate properly formatted HTML table for bonos results"""
    html = '''
    <table class="min-w-full divide-y divide-secondary-200">
        <thead class="bg-secondary-100 sticky top-0">
            <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Periodo</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Flujo (USD)</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-secondary-600 uppercase tracking-wider">Valor Presente (USD)</th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-secondary-200">
    '''

    for _, row in dataframe.iterrows():
        html += f'''
            <tr class="hover:bg-secondary-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-secondary-900">{int(row['Periodo'])}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">${row['Flujo (USD)']:.2f}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">${row['Valor Presente (USD)']:.2f}</td>
            </tr>
        '''

    html += '''
        </tbody>
    </table>
    '''

    return html

def generate_bonos_table_rows_html(dataframe):
    """Generate only the table rows HTML for bonos results (for AJAX updates)"""
    html = ''

    for _, row in dataframe.iterrows():
        html += f'''
            <tr class="hover:bg-secondary-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-secondary-900">{int(row['Periodo'])}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">${row['Flujo (USD)']:.2f}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">${row['Valor Presente (USD)']:.2f}</td>
            </tr>
        '''

    return html

@main.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main.route('/cartera', methods=['GET', 'POST'])
def cartera():
    """Módulo A: Crecimiento de Cartera"""
    form = CarteraForm()
    resultado = None
    errors = []

    if request.method == 'POST':
        if form.validate():
            # Process form data
            tipo_plazo = form.tipo_plazo.data
            años_data = form.años.data if hasattr(form.años, 'data') else None
            edad_retiro_data = form.edad_retiro.data if hasattr(form.edad_retiro, 'data') else None

            datos = {
                'edad_actual': form.edad_actual.data,
                'monto_inicial': form.monto_inicial.data,
                'aporte_periodico': form.aporte_periodico.data,
                'frecuencia': form.frecuencia.data,
                'tipo_plazo': tipo_plazo,
                'años': años_data if tipo_plazo == 'años' and años_data is not None else None,
                'edad_retiro': edad_retiro_data if tipo_plazo == 'edad' and edad_retiro_data is not None else None,
                'tea': form.tea.data
            }

            try:
                resultado = calcular_cartera(datos)
                # Store results in session for use by other modules (exclude DataFrame)
                session['cartera_resumen'] = resultado['resumen']
                session['cartera_datos'] = datos

                # Auto-save simulation to database
                try:
                    simulation_name = f"Simulación Cartera - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    simulation = Simulation(
                        user_id=g.user.id,
                        name=simulation_name,
                        description="Cálculo automático de crecimiento de cartera",
                        module_type='cartera',
                        input_data=datos,
                        results_data={
                            'resumen': resultado['resumen'],
                            'dataframe': resultado['dataframe'].to_dict('records')
                        }
                    )
                    db.session.add(simulation)
                    db.session.commit()

                    # Update user stats and check achievements
                    update_user_stats(g.user.id)
                    awarded_achievements = check_achievements(g.user.id)
                except Exception as db_error:
                    # Don't fail the calculation if database save fails
                    print(f"Database save error: {db_error}")
                    awarded_achievements = []

                # Return JSON for AJAX requests
                if is_ajax_request():
                    # Generate properly formatted table HTML
                    table_html = generate_cartera_table_html(resultado['dataframe'])
                    # Generate summary view HTML
                    summary_html = generate_cartera_summary_html(resultado['dataframe'])
                    return jsonify({
                        'success': True,
                        'resultado': {
                            'resumen': resultado['resumen'],
                            'dataframe_html': table_html,
                            'summary_html': summary_html
                        },
                        'awarded_achievements': [a.to_dict() for a in awarded_achievements] if awarded_achievements else []
                    })
            except Exception as e:
                error_msg = f'Error en el cálculo: {str(e)}'
                if is_ajax_request():
                    return jsonify({'success': False, 'error': error_msg})
                flash(error_msg, 'error')
        else:
            # Form validation errors
            errors = [field.errors for field in form if field.errors]
            if is_ajax_request():
                return jsonify({'success': False, 'errors': errors})

    # Return HTML for regular requests
    return render_template('cartera.html', form=form, resultado=resultado, errors=errors)

@main.route('/jubilacion', methods=['GET', 'POST'])
def jubilacion():
    """Módulo B: Proyección de Jubilación"""
    form = JubilacionForm()
    resultado = None
    modulo_a_completado = 'cartera_resumen' in session
    errors = []

    if request.method == 'POST':
        if form.validate():
            if not modulo_a_completado:
                error_msg = 'Debes completar primero el Módulo A (Crecimiento de Cartera)'
                if is_ajax_request():
                    return jsonify({'success': False, 'error': error_msg})
                flash(error_msg, 'error')
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

                # Return JSON for AJAX requests
                if is_ajax_request():
                    return jsonify({
                        'success': True,
                        'resultado': resultado,
                        'modulo_a_completado': modulo_a_completado
                    })
            except Exception as e:
                error_msg = f'Error en el cálculo: {str(e)}'
                if is_ajax_request():
                    return jsonify({'success': False, 'error': error_msg})
                flash(error_msg, 'error')
        else:
            # Form validation errors
            errors = [field.errors for field in form if field.errors]
            if is_ajax_request():
                return jsonify({'success': False, 'errors': errors})

    # Return HTML for regular requests
    return render_template('jubilacion.html', form=form, resultado=resultado, modulo_a_completado=modulo_a_completado, errors=errors)

@main.route('/bonos', methods=['GET', 'POST'])
def bonos():
    """Módulo C: Valoración de Bonos"""
    form = BonosForm()
    resultado = None
    errors = []

    if request.method == 'POST':
        if form.validate():
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
                # Store results in session for PDF download (convert DataFrame to dict)
                session['bonos_resultado'] = {
                    'dataframe': resultado['dataframe'].to_dict('records'),
                    'resumen': resultado['resumen']
                }

                # Return JSON for AJAX requests
                if is_ajax_request():
                    # Generate table rows HTML for AJAX updates
                    table_rows_html = generate_bonos_table_rows_html(resultado['dataframe'])
                    return jsonify({
                        'success': True,
                        'resultado': {
                            'resumen': resultado['resumen'],
                            'dataframe': resultado['dataframe'].to_dict('records'),
                            'dataframe_html': table_rows_html
                        }
                    })
            except Exception as e:
                error_msg = f'Error en el cálculo: {str(e)}'
                if is_ajax_request():
                    return jsonify({'success': False, 'error': error_msg})
                flash(error_msg, 'error')
        else:
            # Form validation errors
            errors = [field.errors for field in form if field.errors]
            if is_ajax_request():
                return jsonify({'success': False, 'errors': errors})

    # Return HTML for regular requests
    return render_template('bonos.html', form=form, resultado=resultado, errors=errors)

@main.route('/resultado')
def resultado():
    """Mostrar resultados detallados"""
    return render_template('resultado.html')

@main.route('/descargar-pdf/<modulo>')
def descargar_pdf(modulo):
    """Download PDF report for the specified module"""
    try:
        if modulo == 'cartera':
            # Check if portfolio data exists in session
            if 'cartera_resumen' not in session:
                flash('Debes completar primero el Módulo A (Crecimiento de Cartera)', 'error')
                return redirect(url_for('main.cartera'))

            # Recalculate to get the dataframe
            datos = session.get('cartera_datos', {})
            resultado = calcular_cartera(datos)

            # Merge original parameters with summary for PDF
            resumen_completo = resultado['resumen'].copy()
            resumen_completo.update({
                'edad_actual': datos.get('edad_actual'),
                'monto_inicial': datos.get('monto_inicial'),
                'aporte_periodico': datos.get('aporte_periodico'),
                'frecuencia': datos.get('frecuencia'),
                'tipo_plazo': datos.get('tipo_plazo'),
                'años': datos.get('años'),
                'edad_retiro': datos.get('edad_retiro'),
                'tea': datos.get('tea')
            })

            # Generate PDF with complete data
            pdf_buffer = generar_pdf_cartera(resultado['dataframe'], resumen_completo)
            pdf_buffer.seek(0)

            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=f'reporte_cartera_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )

        elif modulo == 'bonos':
            # Check if bond data exists in session
            if 'bonos_resultado' not in session:
                flash('Debes completar primero el Módulo C (Valoración de Bonos)', 'error')
                return redirect(url_for('main.bonos'))

            # Get data from session and convert back to DataFrame
            session_data = session['bonos_resultado']
            import pandas as pd
            resultado = {
                'dataframe': pd.DataFrame(session_data['dataframe']),
                'resumen': session_data['resumen']
            }

            # Generate PDF
            pdf_buffer = generar_pdf_bono(resultado['dataframe'], resultado['resumen'])
            pdf_buffer.seek(0)

            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=f'reporte_bonos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )

        elif modulo == 'jubilacion':
            # Check if retirement data exists in session
            if 'jubilacion_resultado' not in session:
                flash('Debes completar primero el Módulo B (Proyección de Jubilación)', 'error')
                return redirect(url_for('main.jubilacion'))

            # Get data from session
            resultado = session['jubilacion_resultado']

            # Generate PDF
            pdf_buffer = generar_pdf_jubilacion(resultado)
            pdf_buffer.seek(0)

            return send_file(
                pdf_buffer,
                as_attachment=True,
                download_name=f'reporte_jubilacion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )

        else:
            flash('Módulo no válido', 'error')
            return redirect(url_for('main.index'))

    except Exception as e:
        flash(f'Error al generar el PDF: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@main.route('/escenarios-sensibilidad')
@login_required
def escenarios_sensibilidad():
    """Módulo D: Escenarios de Sensibilidad y Análisis de Riesgo"""
    # Check if portfolio data exists in session
    if 'cartera_resumen' not in session or 'cartera_datos' not in session:
        flash('Debes completar primero el Módulo A (Crecimiento de Cartera) para usar escenarios de sensibilidad', 'error')
        return redirect(url_for('main.cartera'))

    return render_template('escenarios_sensibilidad.html')

@main.route('/modulo-inflacion')
@login_required
def modulo_inflacion():
    """Módulo E: Inflación y Ajustes Automáticos"""
    # Check if portfolio data exists in session
    if 'cartera_resumen' not in session or 'cartera_datos' not in session:
        flash('Debes completar primero el Módulo A (Crecimiento de Cartera) para usar el módulo de inflación', 'error')
        return redirect(url_for('main.cartera'))

    return render_template('modulo_inflacion.html')

@main.route('/comparador-estrategias')
@login_required
def comparador_estrategias():
    """Módulo F: Comparador de Estrategias de Inversión"""
    # Check if portfolio data exists in session
    if 'cartera_resumen' not in session or 'cartera_datos' not in session:
        flash('Debes completar primero el Módulo A (Crecimiento de Cartera) para usar el comparador de estrategias', 'error')
        return redirect(url_for('main.cartera'))

    return render_template('comparador_estrategias.html')

@main.route('/api/calcular-escenario', methods=['POST'])
def calcular_escenario():
    """API endpoint for real-time scenario calculations"""
    try:
        data = request.get_json()

        # Get base portfolio data from session
        base_datos = session.get('cartera_datos', {})
        if not base_datos:
            return jsonify({'success': False, 'error': 'Datos base no encontrados'})

        # Apply sensitivity changes
        datos_modificados = base_datos.copy()

        # Apply percentage changes to variables
        if 'tea_change' in data:
            tea_change = data['tea_change'] / 100  # Convert percentage to decimal
            datos_modificados['tea'] = base_datos['tea'] * (1 + tea_change)

        if 'aporte_change' in data:
            aporte_change = data['aporte_change'] / 100
            datos_modificados['aporte_periodico'] = base_datos['aporte_periodico'] * (1 + aporte_change)

        if 'inflacion_change' in data:
            # Apply inflation adjustment (simplified model)
            inflacion_change = data['inflacion_change'] / 100
            # Reduce future value by inflation
            datos_modificados['tea'] = base_datos['tea'] - (inflacion_change * 100)  # Rough approximation

        # Handle edad_retiro parameter for retirement age comparison
        if 'edad_retiro' in data:
            edad_retiro = data['edad_retiro']
            edad_actual = base_datos.get('edad_actual', 30)  # Default to 30 if not available
            años_calculo = max(1, edad_retiro - edad_actual)  # Ensure at least 1 year

            # Override the calculation period
            datos_modificados['tipo_plazo'] = 'años'
            datos_modificados['años'] = años_calculo
            datos_modificados.pop('edad_retiro', None)  # Remove if present

        # Calculate with modified data
        resultado = calcular_cartera(datos_modificados)

        return jsonify({
            'success': True,
            'resultado': {
                'capital_final': resultado['resumen']['capital_final'],
                'aportes_totales': resultado['resumen']['aportes_totales'],
                'ganancia_bruta': resultado['resumen']['ganancia_bruta'],
                'rentabilidad': resultado['resumen']['rentabilidad']
            }
        })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in calcular_escenario: {str(e)}")
        print(f"Traceback: {error_details}")
        return jsonify({'success': False, 'error': f'Error al calcular escenario: {str(e)}'})

@main.route('/api/analisis-riesgo', methods=['POST'])
def analisis_riesgo():
    """API endpoint for risk analysis with multiple scenarios"""
    try:
        # Get base portfolio data from session
        base_datos = session.get('cartera_datos', {})
        if not base_datos:
            return jsonify({'success': False, 'error': 'Datos base no encontrados'})

        # Define risk scenarios
        escenarios = {
            'optimista': {'tea_multiplier': 1.3, 'aporte_multiplier': 1.1},  # +30% TEA, +10% aportes
            'base': {'tea_multiplier': 1.0, 'aporte_multiplier': 1.0},       # Caso base
            'pesimista': {'tea_multiplier': 0.7, 'aporte_multiplier': 0.9},  # -30% TEA, -10% aportes
            'volatil': {'tea_multiplier': 1.0, 'volatility': 0.2}            # Con volatilidad
        }

        resultados = {}

        for nombre, ajustes in escenarios.items():
            datos_escenario = base_datos.copy()

            if nombre == 'volatil':
                # Generate multiple simulations with volatility
                simulaciones = []
                base_tea = base_datos['tea']

                for i in range(100):  # 100 simulations
                    # Add random variation (±20%)
                    variation = np.random.normal(0, ajustes.get('volatility', 0.1))
                    datos_escenario['tea'] = base_tea * (1 + variation)

                    try:
                        resultado = calcular_cartera(datos_escenario)
                        simulaciones.append(resultado['resumen']['capital_final'])
                    except:
                        continue

                if simulaciones:
                    resultados[nombre] = {
                        'capital_final_promedio': np.mean(simulaciones),
                        'capital_final_min': np.min(simulaciones),
                        'capital_final_max': np.max(simulaciones),
                        'desviacion_estandar': np.std(simulaciones),
                        'percentil_10': np.percentile(simulaciones, 10),
                        'percentil_90': np.percentile(simulaciones, 90)
                    }
            else:
                # Standard scenario calculation
                datos_escenario['tea'] = base_datos['tea'] * ajustes['tea_multiplier']
                datos_escenario['aporte_periodico'] = base_datos['aporte_periodico'] * ajustes['aporte_multiplier']

                resultado = calcular_cartera(datos_escenario)
                resultados[nombre] = resultado['resumen']

        return jsonify({'success': True, 'resultados': resultados})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main.route('/descargar-manual')
def descargar_manual():
    """Download user manual PDF"""
    try:
        # Generate the manual PDF
        manual_path = crear_manual_usuario()

        return send_file(
            manual_path,
            as_attachment=True,
            download_name='manual_usuario_simulador_financiero.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        flash(f'Error al generar el manual: {str(e)}', 'error')
        return redirect(url_for('main.index'))

@main.route('/api/calcular-inflacion', methods=['POST'])
def calcular_inflacion():
    """API endpoint for inflation-adjusted calculations"""
    try:
        data = request.get_json()

        # Get base portfolio data from session
        base_datos = session.get('cartera_datos', {})
        if not base_datos:
            return jsonify({'success': False, 'error': 'Datos base no encontrados. Complete el Módulo A primero.'})

        # Ensure 'tea' key exists
        if 'tea' not in base_datos:
            return jsonify({'success': False, 'error': 'Datos de TEA no encontrados. Complete el Módulo A primero.'})

        # Apply inflation adjustments
        tasa_inflacion = data.get('tasa_inflacion', 0.03)
        escalado_aportes = data.get('escalado_aportes', 0.0)
        reajuste_jubilacion = data.get('reajuste_jubilacion', False)

        # Calculate with inflation adjustments
        df_inflacion, resumen_inflacion = simular_cartera_con_inflacion(
            monto_inicial=base_datos['monto_inicial'],
            aporte_inicial=base_datos['aporte_periodico'],
            tea=base_datos['tea'],
            frecuencia=base_datos['frecuencia'],
            años=base_datos.get('años', 25),
            tasa_inflacion=tasa_inflacion,
            escalado_aportes=escalado_aportes,
            reajuste_jubilacion=reajuste_jubilacion
        )

        return jsonify({
            'success': True,
            'resumen': resumen_inflacion,
            'dataframe': df_inflacion.to_dict('records')
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/comparar-estrategias', methods=['POST'])
def comparar_estrategias():
    """API endpoint for strategy comparison"""
    try:
        data = request.get_json()

        # Get base portfolio data from session
        base_datos = session.get('cartera_datos', {})
        if not base_datos:
            return jsonify({'success': False, 'error': 'Datos base no encontrados. Complete el Módulo A primero.'})

        estrategias_seleccionadas = data.get('estrategias', [])
        estrategia_personalizada = data.get('estrategia_personalizada')
        rebalanceo = data.get('rebalanceo', 'none')

        print(f"Debug: estrategias_seleccionadas = {estrategias_seleccionadas}")
        print(f"Debug: estrategia_personalizada = {estrategia_personalizada}")
        print(f"Debug: rebalanceo = {rebalanceo}")
        print(f"Debug: base_datos = {base_datos}")

        # Validate input data
        if not estrategias_seleccionadas:
            return jsonify({'success': False, 'error': 'Debes seleccionar al menos una estrategia para comparar'})

        # Define strategy configurations
        estrategias_config = {
            'conservative': [
                {'nombre': 'Bonos', 'peso': 0.7, 'tea': 0.04},
                {'nombre': 'Acciones', 'peso': 0.3, 'tea': 0.08}
            ],
            'moderate': [
                {'nombre': 'Bonos', 'peso': 0.5, 'tea': 0.04},
                {'nombre': 'Acciones', 'peso': 0.5, 'tea': 0.08}
            ],
            'aggressive': [
                {'nombre': 'Bonos', 'peso': 0.2, 'tea': 0.04},
                {'nombre': 'Acciones', 'peso': 0.8, 'tea': 0.08}
            ],
            'balanced': [
                {'nombre': 'Bonos', 'peso': 0.4, 'tea': 0.04},
                {'nombre': 'Acciones', 'peso': 0.4, 'tea': 0.08},
                {'nombre': 'Oro', 'peso': 0.2, 'tea': 0.03}
            ],
            'tech': [
                {'nombre': 'Tech Stocks', 'peso': 0.7, 'tea': 0.12},
                {'nombre': 'Bonos', 'peso': 0.3, 'tea': 0.04}
            ]
        }

        # Prepare strategies for comparison
        estrategias_comparar = []

        for estrategia in estrategias_seleccionadas:
            if estrategia == 'custom' and estrategia_personalizada:
                # Custom strategy - calculate weighted average TEA
                tea_custom = 0
                total_weight = 0
                if estrategia_personalizada.get('stocks', 0) > 0:
                    tea_custom += (estrategia_personalizada['stocks'] / 100) * 0.08
                    total_weight += estrategia_personalizada['stocks'] / 100
                if estrategia_personalizada.get('bonds', 0) > 0:
                    tea_custom += (estrategia_personalizada['bonds'] / 100) * 0.04
                    total_weight += estrategia_personalizada['bonds'] / 100
                if estrategia_personalizada.get('gold', 0) > 0:
                    tea_custom += (estrategia_personalizada['gold'] / 100) * 0.03
                    total_weight += estrategia_personalizada['gold'] / 100
                if estrategia_personalizada.get('realEstate', 0) > 0:
                    tea_custom += (estrategia_personalizada['realEstate'] / 100) * 0.06
                    total_weight += estrategia_personalizada['realEstate'] / 100

                if total_weight > 0:
                    tea_custom = tea_custom / total_weight
                else:
                    tea_custom = 0.05  # Default

                estrategias_comparar.append({
                    'nombre': 'Personalizada',
                    'tea': tea_custom,
                    'volatilidad': 0.15,  # Higher volatility for custom
                    'rebalanceo': rebalanceo != 'none'
                })
            elif estrategia in estrategias_config:
                # Calculate weighted average TEA for predefined strategies
                activos = estrategias_config[estrategia]
                tea_estrategia = sum(activo['peso'] * activo['tea'] for activo in activos)

                # Map strategy names to Spanish
                nombre_estrategia = {
                    'conservative': 'Conservadora',
                    'moderate': 'Moderada',
                    'aggressive': 'Agresiva',
                    'balanced': 'Balanceada',
                    'tech': 'Tecnología'
                }.get(estrategia, estrategia.title())

                estrategias_comparar.append({
                    'nombre': nombre_estrategia,
                    'tea': tea_estrategia,
                    'volatilidad': 0.10 if estrategia == 'conservative' else 0.15 if estrategia == 'moderate' else 0.20 if estrategia == 'aggressive' else 0.18,
                    'rebalanceo': rebalanceo != 'none'
                })

        print(f"Debug: estrategias_comparar = {estrategias_comparar}")

        if not estrategias_comparar:
            return jsonify({'success': False, 'error': 'No se pudieron preparar las estrategias para comparar'})

        # Compare strategies
        print(f"Debug: About to call comparar_estrategias_inversion with:")
        print(f"  monto_inicial: {base_datos['monto_inicial']}")
        print(f"  aporte_periodico: {base_datos['aporte_periodico']}")
        print(f"  frecuencia: {base_datos['frecuencia']}")
        print(f"  años: {base_datos.get('años', 25)}")

        df_comparacion = comparar_estrategias_inversion(
            monto_inicial=base_datos['monto_inicial'],
            aporte_periodico=base_datos['aporte_periodico'],
            frecuencia=base_datos['frecuencia'],
            años=base_datos.get('años', 25),
            estrategias=estrategias_comparar
        )
        print(f"Debug: comparar_estrategias_inversion completed successfully")

        # Calculate benchmarks
        print(f"Debug: About to call calcular_benchmarking")
        benchmarks = [
            {'nombre': 'S&P 500', 'tea': 0.08},
            {'nombre': 'Bonos del Tesoro', 'tea': 0.04},
            {'nombre': 'Oro', 'tea': 0.03},
            {'nombre': 'Bienes Raíces', 'tea': 0.06}
        ]

        df_benchmarks = calcular_benchmarking(
            estrategia_personal={'tea': base_datos['tea']},
            benchmarks=benchmarks,
            monto_inicial=base_datos['monto_inicial'],
            aporte_periodico=base_datos['aporte_periodico'],
            frecuencia=base_datos['frecuencia'],
            años=base_datos.get('años', 25)
        )
        print(f"Debug: calcular_benchmarking completed successfully")

        # Calculate risk analysis using the same activos structure
        print(f"Debug: Starting risk analysis")
        capitales_simulados = []
        for estrategia in estrategias_seleccionadas:
            print(f"Debug: Processing estrategia: {estrategia}")
            if estrategia == 'custom' and estrategia_personalizada:
                # Use custom activos for risk analysis
                activos_riesgo = []
                if estrategia_personalizada.get('stocks', 0) > 0:
                    activos_riesgo.append({'nombre': 'Acciones', 'peso': estrategia_personalizada['stocks'] / 100, 'tea': 0.08})
                if estrategia_personalizada.get('bonds', 0) > 0:
                    activos_riesgo.append({'nombre': 'Bonos', 'peso': estrategia_personalizada['bonds'] / 100, 'tea': 0.04})
                if estrategia_personalizada.get('gold', 0) > 0:
                    activos_riesgo.append({'nombre': 'Oro', 'peso': estrategia_personalizada['gold'] / 100, 'tea': 0.03})
                if estrategia_personalizada.get('realEstate', 0) > 0:
                    activos_riesgo.append({'nombre': 'Bienes Raíces', 'peso': estrategia_personalizada['realEstate'] / 100, 'tea': 0.06})
            elif estrategia in estrategias_config:
                activos_riesgo = estrategias_config[estrategia]
            else:
                continue

            if activos_riesgo:
                df_sim, _ = simular_rebalanceo_automatico(
                    monto_inicial=base_datos['monto_inicial'],
                    aporte_periodico=base_datos['aporte_periodico'],
                    frecuencia=base_datos['frecuencia'],
                    años=base_datos.get('años', 25),
                    activos=activos_riesgo,
                    frecuencia_rebalanceo=rebalanceo if rebalanceo != 'none' else 'Anual'
                )
                capitales_simulados.extend(df_sim['Saldo Total (USD)'].tail(10).tolist())

        if capitales_simulados:
            mejor_escenario = max(capitales_simulados)
            peor_escenario = min(capitales_simulados)
            volatilidad_promedio = np.std(capitales_simulados) / np.mean(capitales_simulados) * 100
            promedio_capital = np.mean(capitales_simulados)
            probabilidad_exito = len([c for c in capitales_simulados if c > promedio_capital * 0.9]) / len(capitales_simulados) * 100
        else:
            mejor_escenario = peor_escenario = volatilidad_promedio = probabilidad_exito = 0

        analisis_riesgo = {
            'volatilidad_promedio': volatilidad_promedio,
            'mejor_escenario': mejor_escenario,
            'peor_escenario': peor_escenario,
            'probabilidad_exito': probabilidad_exito
        }

        return jsonify({
            'success': True,
            'estrategias': df_comparacion.to_dict('records'),
            'benchmarks': df_benchmarks.to_dict('records'),
            'analisis_riesgo': analisis_riesgo
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/exportar-comparacion', methods=['POST'])
def exportar_comparacion():
    """API endpoint for exporting comparison results"""
    try:
        data = request.get_json()

        # Extract data from request
        estrategias = data.get('estrategias', [])
        benchmarks = data.get('benchmarks', [])
        analisis_riesgo = data.get('analisis_riesgo', {})
        configuracion = data.get('configuracion', {})

        # Validate required data
        if not estrategias:
            return jsonify({'success': False, 'error': 'No hay datos de estrategias para exportar'})

        if not benchmarks:
            return jsonify({'success': False, 'error': 'No hay datos de benchmarks para exportar'})

        # Generate PDF
        pdf_buffer = generar_pdf_comparacion(estrategias, benchmarks, analisis_riesgo, configuracion)
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'comparacion_estrategias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in exportar_comparacion: {str(e)}")
        print(f"Traceback: {error_details}")
        return jsonify({'success': False, 'error': f'Error al generar el PDF: {str(e)}'})

@main.route('/api/get-portfolio-data', methods=['GET'])
def get_portfolio_data():
    """API endpoint to get current portfolio data"""
    try:
        if 'cartera_resumen' not in session or 'cartera_datos' not in session:
            return jsonify({'success': False, 'error': 'No portfolio data available'})

        return jsonify({
            'success': True,
            'capital_final': session['cartera_resumen']['capital_final'],
            'aportes_totales': session['cartera_resumen']['aportes_totales'],
            'ganancia_bruta': session['cartera_resumen']['ganancia_bruta']
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ===== USER SYSTEM API ENDPOINTS =====

@main.before_request
def load_user():
    """Load or create user for each request"""
    from flask_login import current_user

    # If user is authenticated via Flask-Login, use that user
    if current_user.is_authenticated:
        g.user = current_user
        # Update session for consistency
        session['user_id'] = current_user.id
        return

    # Otherwise, handle anonymous users
    user_id = session.get('user_id')
    if user_id:
        g.user = get_or_create_user(user_id)
        session['user_id'] = g.user.id
    else:
        g.user = get_or_create_user()
        session['user_id'] = g.user.id

@main.route('/api/user/profile')
def get_user_profile():
    """Get current user profile"""
    try:
        user = g.user
        achievements = UserAchievement.query.filter_by(
            user_id=user.id,
            is_completed=True
        ).all()

        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'achievements': [ua.achievement.to_dict() for ua in achievements]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/user/update-profile', methods=['POST'])
def update_user_profile():
    """Update user profile information"""
    try:
        data = request.get_json()
        user = g.user

        if 'display_name' in data:
            user.display_name = data['display_name']

        if 'preferences' in data:
            user.preferences.update(data['preferences'])

        db.session.commit()

        return jsonify({'success': True, 'user': user.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/simulations', methods=['GET'])
def get_simulations():
    """Get user's simulations"""
    try:
        user = g.user
        simulations = Simulation.query.filter_by(user_id=user.id).order_by(
            Simulation.updated_at.desc()
        ).all()

        return jsonify({
            'success': True,
            'simulations': [s.to_dict() for s in simulations]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/simulations', methods=['POST'])
def save_simulation():
    """Save a new simulation"""
    try:
        data = request.get_json()
        user = g.user

        simulation = Simulation(
            user_id=user.id,
            name=data['name'],
            description=data.get('description', ''),
            module_type=data['module_type'],
            input_data=data['input_data'],
            results_data=data['results_data'],
            is_favorite=data.get('is_favorite', False),
            is_public=data.get('is_public', False)
        )

        db.session.add(simulation)
        db.session.commit()

        # Update user stats and check achievements
        update_user_stats(user.id)
        awarded_achievements = check_achievements(user.id)

        return jsonify({
            'success': True,
            'simulation': simulation.to_dict(),
            'awarded_achievements': [a.to_dict() for a in awarded_achievements]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/simulations/<int:simulation_id>', methods=['GET'])
def get_simulation(simulation_id):
    """Get a specific simulation"""
    try:
        user = g.user
        simulation = Simulation.query.filter_by(
            id=simulation_id,
            user_id=user.id
        ).first()

        if not simulation:
            return jsonify({'success': False, 'error': 'Simulation not found'})

        return jsonify({
            'success': True,
            'simulation': simulation.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/simulations/<int:simulation_id>', methods=['PUT'])
def update_simulation(simulation_id):
    """Update a simulation"""
    try:
        data = request.get_json()
        user = g.user

        simulation = Simulation.query.filter_by(
            id=simulation_id,
            user_id=user.id
        ).first()

        if not simulation:
            return jsonify({'success': False, 'error': 'Simulation not found'})

        # Update fields
        if 'name' in data:
            simulation.name = data['name']
        if 'description' in data:
            simulation.description = data['description']
        if 'is_favorite' in data:
            simulation.is_favorite = data['is_favorite']
        if 'is_public' in data:
            simulation.is_public = data['is_public']

        db.session.commit()

        return jsonify({
            'success': True,
            'simulation': simulation.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/simulations/<int:simulation_id>', methods=['DELETE'])
def delete_simulation(simulation_id):
    """Delete a simulation"""
    try:
        user = g.user
        simulation = Simulation.query.filter_by(
            id=simulation_id,
            user_id=user.id
        ).first()

        if not simulation:
            return jsonify({'success': False, 'error': 'Simulation not found'})

        db.session.delete(simulation)
        db.session.commit()

        # Update user stats
        update_user_stats(user.id)

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/templates', methods=['GET'])
def get_templates():
    """Get public templates and user's own templates"""
    try:
        user = g.user

        # Get user's templates and public templates
        user_templates = Template.query.filter_by(creator_id=user.id).all()
        public_templates = Template.query.filter_by(is_public=True).all()

        # Combine and remove duplicates
        all_templates = list(set(user_templates + public_templates))

        return jsonify({
            'success': True,
            'templates': [t.to_dict() for t in all_templates]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/templates', methods=['POST'])
def create_template():
    """Create a new template"""
    try:
        data = request.get_json()
        user = g.user

        template = Template(
            creator_id=user.id,
            name=data['name'],
            description=data.get('description', ''),
            module_type=data['module_type'],
            template_data=data['template_data'],
            category=data.get('category'),
            tags=data.get('tags', []),
            is_public=data.get('is_public', True)
        )

        db.session.add(template)
        db.session.commit()

        # Update user stats and check achievements
        update_user_stats(user.id)
        awarded_achievements = check_achievements(user.id)

        return jsonify({
            'success': True,
            'template': template.to_dict(),
            'awarded_achievements': [a.to_dict() for a in awarded_achievements]
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/templates/<int:template_id>/vote', methods=['POST'])
def vote_template(template_id):
    """Vote on a template"""
    try:
        data = request.get_json()
        user = g.user
        vote_type = data.get('vote_type')

        if vote_type not in ['upvote', 'downvote']:
            return jsonify({'success': False, 'error': 'Invalid vote type'})

        template = Template.query.get(template_id)
        if not template:
            return jsonify({'success': False, 'error': 'Template not found'})

        # Check if user already voted
        existing_vote = TemplateVote.query.filter_by(
            user_id=user.id,
            template_id=template_id
        ).first()

        if existing_vote:
            # Update existing vote
            old_vote = existing_vote.vote_type
            existing_vote.vote_type = vote_type
        else:
            # Create new vote
            existing_vote = TemplateVote(
                user_id=user.id,
                template_id=template_id,
                vote_type=vote_type
            )
            db.session.add(existing_vote)
            old_vote = None

        # Update template vote counts
        if old_vote == 'upvote':
            template.upvotes -= 1
        elif old_vote == 'downvote':
            template.downvotes -= 1

        if vote_type == 'upvote':
            template.upvotes += 1
        elif vote_type == 'downvote':
            template.downvotes += 1

        db.session.commit()

        return jsonify({
            'success': True,
            'template': template.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/achievements', methods=['GET'])
def get_achievements():
    """Get user's achievement progress"""
    try:
        user = g.user

        user_achievements = UserAchievement.query.filter_by(user_id=user.id).all()
        achievements_dict = {}

        for ua in user_achievements:
            achievements_dict[ua.achievement_id] = {
                'achievement': ua.achievement.to_dict(),
                'progress': ua.to_dict()
            }

        # Include achievements user hasn't started yet
        all_achievements = Achievement.query.filter_by(is_active=True).all()
        for achievement in all_achievements:
            if achievement.id not in achievements_dict:
                # Create progress entry
                user_achievement = UserAchievement(
                    user_id=user.id,
                    achievement_id=achievement.id
                )
                db.session.add(user_achievement)
                achievements_dict[achievement.id] = {
                    'achievement': achievement.to_dict(),
                    'progress': user_achievement.to_dict()
                }

        db.session.commit()

        return jsonify({
            'success': True,
            'achievements': list(achievements_dict.values())
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@main.route('/api/social/comparison')
def get_social_comparison():
    """Get social comparison data"""
    try:
        user = g.user

        # Get user's simulation stats
        user_simulations = Simulation.query.filter_by(user_id=user.id).all()

        if not user_simulations:
            return jsonify({
                'success': True,
                'comparison': {
                    'user_stats': {'total_simulations': 0, 'avg_performance': 0},
                    'community_stats': {'total_users': 0, 'avg_simulations_per_user': 0}
                }
            })

        # Calculate user's average performance
        total_performance = 0
        count = 0
        for sim in user_simulations:
            if sim.results_data and 'resumen' in sim.results_data:
                resumen = sim.results_data['resumen']
                if 'rentabilidad' in resumen:
                    total_performance += resumen['rentabilidad']
                    count += 1

        user_avg_performance = total_performance / count if count > 0 else 0

        # Get community stats (simplified - in production you'd cache this)
        total_users = User.query.count()
        total_simulations = Simulation.query.count()
        avg_simulations_per_user = total_simulations / total_users if total_users > 0 else 0

        return jsonify({
            'success': True,
            'comparison': {
                'user_stats': {
                    'total_simulations': len(user_simulations),
                    'avg_performance': user_avg_performance
                },
                'community_stats': {
                    'total_users': total_users,
                    'avg_simulations_per_user': avg_simulations_per_user
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ===== USER INTERFACE ROUTES =====

@main.route('/perfil/dashboard')
@login_required
def user_dashboard():
    """User dashboard with overview of activity"""
    return render_template('user/dashboard.html')

@main.route('/perfil/simulaciones')
@login_required
def user_simulations():
    """User's saved simulations page"""
    return render_template('user/simulations.html')

@main.route('/perfil/logros')
def user_achievements():
    """User achievements page"""
    return render_template('user/achievements.html')



@main.route('/perfil/comparacion-social')
def social_comparison():
    """Social comparison page"""
    return render_template('user/social_comparison.html')

# ===== AUTHENTICATION ROUTES =====

@main.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.user_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Por favor ingresa email y contraseña', 'error')
            return redirect(url_for('main.login'))

        from .models import User
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            # Update session with registered user
            session['user_id'] = user.id
            flash('¡Bienvenido de vuelta!', 'success')
            return redirect(url_for('main.user_dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'error')

    return render_template('auth/login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.user_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        display_name = request.form.get('display_name')

        if not email or not password or not display_name:
            flash('Por favor completa todos los campos', 'error')
            return redirect(url_for('main.register'))

        from .models import User
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este email ya está registrado', 'error')
            return redirect(url_for('main.register'))

        # Create new registered user
        user = User(
            email=email,
            display_name=display_name.strip(),
            is_registered=True
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        session['user_id'] = user.id

        flash(f'¡Bienvenido, {display_name}! Tu cuenta ha sido creada exitosamente.', 'success')
        return redirect(url_for('main.user_dashboard'))

    return render_template('auth/register.html')

@main.route('/logout')
def logout():
    """User logout"""
    logout_user()
    session.pop('user_id', None)
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('main.index'))
