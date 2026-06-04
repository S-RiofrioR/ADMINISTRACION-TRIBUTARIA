@echo off
echo ========================================
echo Configurando entorno virtual para Analisis de Administracion Tributaria
echo ========================================
echo.

REM Crear entorno virtual
echo [1/4] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual. Asegurate de tener Python instalado.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo [3/4] Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo [4/4] Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

REM Crear carpetas si no existen
echo.
echo Creando estructura de carpetas...
if not exist "DATOS\raw" mkdir "DATOS\raw"
if not exist "DATOS\processed" mkdir "DATOS\processed"
if not exist "DATOS\intermediate" mkdir "DATOS\intermediate"
if not exist "SCRIPTS" mkdir "SCRIPTS"
if not exist "EXPORT\figures" mkdir "EXPORT\figures"
if not exist "EXPORT\tables" mkdir "EXPORT\tables"
if not exist "EXPORT\reports" mkdir "EXPORT\reports"

echo.
echo ========================================
echo ¡Configuracion completada exitosamente!
echo ========================================
echo.
echo Para activar el entorno virtual en el futuro, ejecuta:
echo   venv\Scripts\activate
echo.
echo Luego puedes iniciar Jupyter Notebook con:
echo   jupyter notebook
echo.
pause