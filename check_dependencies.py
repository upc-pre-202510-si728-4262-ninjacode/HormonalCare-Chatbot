#!/usr/bin/env python3
"""
Script para verificar que todas las dependencias estén instaladas correctamente
"""

import sys
import importlib

def check_import(module_name, package_name=None):
    """Verificar si un módulo se puede importar"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name} - ERROR: {e}")
        return False

def main():
    print("🔍 Verificando dependencias del Medical Chatbot...\n")
    
    dependencies = [
        ("flask", "Flask"),
        ("flask_cors", "Flask-CORS"),
        ("flask_restx", "Flask-RESTX"),
        ("google.generativeai", "Google Generative AI"),
        ("dotenv", "Python-dotenv"),
        ("flask_sqlalchemy", "Flask-SQLAlchemy"),
        ("sqlalchemy", "SQLAlchemy"),
        ("requests", "Requests")
    ]
    
    all_good = True
    for module, name in dependencies:
        if not check_import(module, name):
            all_good = False
    
    print(f"\n{'='*50}")
    if all_good:
        print("🎉 ¡Todas las dependencias están instaladas correctamente!")
        print("\n📖 Para iniciar el servidor:")
        print("   python app.py")
        print("\n🌐 Swagger UI estará disponible en:")
        print("   http://localhost:5000/docs/")
    else:
        print("❌ Algunas dependencias faltan. Ejecuta:")
        print("   pip install -r requirements.txt")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
