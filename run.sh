#!/bin/bash

echo "================================================"
echo "   SIMULADOR FINANCIERO DE JUBILACION"
echo "================================================"
echo ""
echo "Iniciando aplicacion..."
echo ""

# Verificar si Python esta instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no esta instalado en el sistema"
    echo "Por favor, instale Python 3.8 o superior"
    exit 1
fi

# Verificar si las dependencias estan instaladas
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Instalando dependencias necesarias..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudieron instalar las dependencias"
        exit 1
    fi
fi

# Iniciar la aplicacion
echo ""
echo "================================================"
echo "La aplicacion se abrira en su navegador"
echo "Presione Ctrl+C para cerrar"
echo "================================================"
echo ""

streamlit run app.py
