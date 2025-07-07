@echo off
echo 🏥 Iniciando Medical Chatbot Backend
echo ==================================

REM Verificar si existe el entorno virtual
if not exist ".venv" (
    echo ❌ Entorno virtual no encontrado. Ejecuta:
    echo    python -m venv .venv
    echo    .venv\Scripts\activate
    echo    pip install -r requirements.txt
    exit /b 1
)

REM Verificar si existe el archivo .env
if not exist ".env" (
    echo ⚠️  Archivo .env no encontrado. Copiando desde .env.example...
    copy .env.example .env
    echo ✅ Archivo .env creado. Por favor configura tu GEMINI_API_KEY antes de continuar.
    exit /b 1
)

REM Verificar si GEMINI_API_KEY está configurada
findstr /C:"GEMINI_API_KEY=your_gemini_api_key_here" .env >nul
if %errorlevel% equ 0 (
    echo ❌ Por favor configura tu GEMINI_API_KEY en el archivo .env
    exit /b 1
) else (
    echo ✅ GEMINI_API_KEY configurada
)

echo 🚀 Iniciando servidor...
python app.py
