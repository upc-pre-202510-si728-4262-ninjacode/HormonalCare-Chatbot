@echo off
echo 🔧 Instalación paso a paso...
echo ===========================

echo Instalando Flask y extensiones básicas...
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install werkzeug

echo Instalando Flask-RESTX...
pip install flask-restx==1.3.0

echo Instalando Google AI...
pip install google-generativeai==0.3.2

echo Instalando utilidades...
pip install python-dotenv==1.0.0
pip install pydantic==2.5.2
pip install typing-extensions==4.8.0
pip install requests==2.31.0

echo Instalando base de datos...
pip install sqlalchemy==2.0.23
pip install flask-sqlalchemy==3.1.1

echo ✅ Verificando instalación...
python check_dependencies.py

pause
