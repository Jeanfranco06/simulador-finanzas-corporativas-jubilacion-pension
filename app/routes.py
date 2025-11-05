from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, send_file
from .forms import CarteraForm, JubilacionForm, BonosForm
from .models import calcular_cartera, calcular_jubilacion, calcular_bonos
from utils.pdf_generator import generar_pdf_cartera, generar_pdf_bono, generar_pdf_jubilacion
from datetime import datetime

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
                # Store results in session for PDF download
                session['bonos_resultado'] = resultado

                # Return JSON for AJAX requests
                if is_ajax_request():
                    # Generate properly formatted table HTML for bonds
                    table_html = generate_bonos_table_html(resultado['dataframe'])
                    return jsonify({
                        'success': True,
                        'resultado': {
                            'resumen': resultado['resumen'],
                            'dataframe': resultado['dataframe'].to_dict('records'),
                            'dataframe_html': table_html
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

            # Get data from session
            resultado = session['bonos_resultado']

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
