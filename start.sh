#!/bin/bash

echo "🏥 Iniciando Medical Chatbot Backend"
echo "=================================="

# Verificar si existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado. Por favor configura tu GEMINI_API_KEY antes de continuar."
    exit 1
fi

# Verificar si GEMINI_API_KEY está configurada
if ! grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
    echo "✅ GEMINI_API_KEY configurada"
else
    echo "❌ Por favor configura tu GEMINI_API_KEY en el archivo .env"
    exit 1
fi

echo "🚀 Iniciando servidor..."
python app.py
