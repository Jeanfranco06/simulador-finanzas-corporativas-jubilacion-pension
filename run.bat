@echo off
echo ================================================
echo   SIMULADOR FINANCIERO DE JUBILACION
echo ================================================
echo.
echo Iniciando aplicacion...
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado en el sistema
    echo Por favor, instale Python 3.8 o superior desde python.org
    pause
    exit /b 1
)

REM Verificar si las dependencias estan instaladas
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias necesarias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

REM Iniciar la aplicacion
echo.
echo ================================================
echo La aplicacion se abrira en su navegador
echo Presione Ctrl+C para cerrar
echo ================================================
echo.

streamlit run app.py

pause
