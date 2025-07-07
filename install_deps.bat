@echo off
echo 🔧 Limpiando e instalando dependencias...
echo ==========================================

echo 📦 Actualizando pip...
python -m pip install --upgrade pip

echo 🧹 Limpiando cache de pip...
pip cache purge

echo 📥 Instalando dependencias...
pip install -r requirements.txt

echo ✅ Verificando instalación...
python check_dependencies.py

echo.
echo 🚀 Si todo está OK, ejecuta: python app.py
pause
