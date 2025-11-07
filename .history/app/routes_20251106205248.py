from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, send_file
from .forms import CarteraForm, JubilacionForm, BonosForm
from .models import calcular_cartera, calcular_jubilacion, calcular_bonos
from utils.pdf_generator import generar_pdf_cartera, generar_pdf_bono, generar_pdf_jubilacion
from utils.manual_usuario import crear_manual_usuario
from utils.calculos_financieros import (
    calcular_cartera_con_inflacion,
    comparar_estrategias_inversion,
    calcular_benchmarking,
    simular_rebalanceo_automatico
)
from datetime import datetime
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
def escenarios_sensibilidad():
    """Módulo D: Escenarios de Sensibilidad y Análisis de Riesgo"""
    # Check if portfolio data exists in session
    if 'cartera_resumen' not in session or 'cartera_datos' not in session:
        flash('Debes completar primero el Módulo A (Crecimiento de Cartera) para usar escenarios de sensibilidad', 'error')
        return redirect(url_for('main.cartera'))

    return render_template('escenarios_sensibilidad.html')

@main.route('/modulo-inflacion')
def modulo_inflacion():
    """Módulo E: Inflación y Ajustes Automáticos"""
    # Check if portfolio data exists in session
    if 'cartera_resumen' not in session or 'cartera_datos' not in session:
        flash('Debes completar primero el Módulo A (Crecimiento de Cartera) para usar el módulo de inflación', 'error')
        return redirect(url_for('main.cartera'))

    return render_template('modulo_inflacion.html')

@main.route('/comparador-estrategias')
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
        return jsonify({'success': False, 'error': str(e)})

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

        # Apply inflation adjustments
        tasa_inflacion = data.get('tasa_inflacion', 0.03)
        escalado_aportes = data.get('escalado_aportes', 0.0)
        reajuste_jubilacion = data.get('reajuste_jubilacion', False)

        # Calculate with inflation adjustments
        df_inflacion, resumen_inflacion = calcular_cartera_con_inflacion(
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
                # Custom strategy
                activos_custom = []
                if estrategia_personalizada.get('stocks', 0) > 0:
                    activos_custom.append({'nombre': 'Acciones', 'peso': estrategia_personalizada['stocks'] / 100, 'tea': 0.08})
                if estrategia_personalizada.get('bonds', 0) > 0:
                    activos_custom.append({'nombre': 'Bonos', 'peso': estrategia_personalizada['bonds'] / 100, 'tea': 0.04})
                if estrategia_personalizada.get('gold', 0) > 0:
                    activos_custom.append({'nombre': 'Oro', 'peso': estrategia_personalizada['gold'] / 100, 'tea': 0.03})
                if estrategia_personalizada.get('realEstate', 0) > 0:
                    activos_custom.append({'nombre': 'Bienes Raíces', 'peso': estrategia_personalizada['realEstate'] / 100, 'tea': 0.06})

                estrategias_comparar.append({
                    'nombre': 'Personalizada',
                    'activos': activos_custom,
                    'rebalanceo': rebalanceo != 'none'
                })
            elif estrategia in estrategias_config:
                estrategias_comparar.append({
                    'nombre': estrategia.title(),
                    'activos': estrategias_config[estrategia],
                    'rebalanceo': rebalanceo != 'none'
                })

        # Compare strategies
        df_comparacion = comparar_estrategias_inversion(
            monto_inicial=base_datos['monto_inicial'],
            aporte_periodico=base_datos['aporte_periodico'],
            frecuencia=base_datos['frecuencia'],
            años=base_datos.get('años', 25),
            estrategias=estrategias_comparar
        )

        # Calculate benchmarks
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

        # Calculate risk analysis
        capitales_simulados = []
        for estrategia in estrategias_comparar:
            if estrategia['activos']:
                df_sim, _ = simular_rebalanceo_automatico(
                    monto_inicial=base_datos['monto_inicial'],
                    aporte_periodico=base_datos['aporte_periodico'],
                    frecuencia=base_datos['frecuencia'],
                    años=base_datos.get('años', 25),
                    activos=estrategia['activos'],
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
        # This would generate a PDF report - simplified version
        return jsonify({'success': True, 'message': 'Export functionality would be implemented here'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

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
