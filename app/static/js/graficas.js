/**
 * JavaScript functions for charts and interactive elements
 * Financial Simulator
 */

// Global chart instances to avoid memory leaks
let chartInstances = {};

// Function to create portfolio growth chart
function crearGraficaCartera(datos) {
    const ctx = document.getElementById('graficaCartera');
    if (!ctx) return;

    // Destroy existing chart
    if (chartInstances.cartera) {
        chartInstances.cartera.destroy();
    }

    const labels = datos.map(item => `Periodo ${item.periodo}`);
    const saldoTotal = datos.map(item => item.saldo_final);
    const aportesAcumulados = datos.map(item => item.aportes_acumulados);

    chartInstances.cartera = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Saldo Total',
                data: saldoTotal,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
            }, {
                label: 'Aportes Acumulados',
                data: aportesAcumulados,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Evolución de la Cartera'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// Function to create bond valuation chart
function crearGraficaBonos(datos) {
    const ctx = document.getElementById('graficaBonos');
    if (!ctx) return;

    // Destroy existing chart
    if (chartInstances.bonos) {
        chartInstances.bonos.destroy();
    }

    const labels = datos.map(item => `Periodo ${item.periodo}`);
    const flujos = datos.map(item => item.flujo);
    const valoresPresentes = datos.map(item => item.valor_presente);

    chartInstances.bonos = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Flujo Nominal',
                data: flujos,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }, {
                label: 'Valor Presente',
                data: valoresPresentes,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Flujos del Bono y sus Valores Presentes'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// Function to show loading state
function mostrarCargando(elemento, mostrar = true) {
    if (mostrar) {
        elemento.classList.add('loading');
    } else {
        elemento.classList.remove('loading');
    }
}

// Function to format currency
function formatearMoneda(valor) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(valor);
}

// Function to format percentage
function formatearPorcentaje(valor) {
    return (valor * 100).toFixed(2) + '%';
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculando...';
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Clean up charts when page unloads
window.addEventListener('beforeunload', function() {
    Object.values(chartInstances).forEach(chart => {
        if (chart) {
            chart.destroy();
        }
    });
    chartInstances = {};
});
