#!/usr/bin/env python3
"""
Script para probar la creación de usuarios en MySQL
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
from src.infrastructure.database import db, UserModel
from flask import Flask

# Cargar variables de entorno
load_dotenv()

def create_app():
    """Crear aplicación Flask para acceder a la base de datos"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def test_create_user():
    """Probar la creación de un usuario"""
    app = create_app()
    
    with app.app_context():
        print("🧪 Probando creación de usuario en MySQL...")
        print("=" * 45)
        
        try:
            # Crear un usuario de prueba
            test_user = UserModel(
                id="test-user-123",
                name="Usuario de Prueba",
                age=30,
                gender="masculino",
                created_at=datetime.utcnow()
            )
            
            print(f"📝 Creando usuario: {test_user.name}")
            
            # Guardar en la base de datos
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Usuario guardado exitosamente")
            
            # Verificar que se guardó
            saved_user = UserModel.query.filter_by(id="test-user-123").first()
            if saved_user:
                print(f"✅ Usuario encontrado en BD: {saved_user.name}")
                print(f"   ID: {saved_user.id}")
                print(f"   Edad: {saved_user.age}")
                print(f"   Género: {saved_user.gender}")
                print(f"   Creado: {saved_user.created_at}")
            else:
                print("❌ Usuario no encontrado después de guardarlo")
            
            # Contar total de usuarios
            total_users = UserModel.query.count()
            print(f"📊 Total de usuarios en BD: {total_users}")
            
            # Limpiar el usuario de prueba
            if saved_user:
                db.session.delete(saved_user)
                db.session.commit()
                print("🗑️  Usuario de prueba eliminado")
            
        except Exception as e:
            print(f"❌ Error durante la prueba: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

def test_list_users():
    """Listar todos los usuarios actuales"""
    app = create_app()
    
    with app.app_context():
        print("\n👥 Usuarios actuales en la base de datos:")
        print("=" * 40)
        
        try:
            users = UserModel.query.all()
            if users:
                for i, user in enumerate(users, 1):
                    print(f"{i}. {user.name} (ID: {user.id})")
                    print(f"   Edad: {user.age}, Género: {user.gender}")
                    print(f"   Creado: {user.created_at}")
                    print()
            else:
                print("📭 No hay usuarios en la base de datos")
                
        except Exception as e:
            print(f"❌ Error listando usuarios: {e}")

def main():
    """Función principal"""
    print("🏥 Test de Usuarios - Medical Chatbot")
    print("=" * 40)
    
    # Listar usuarios actuales
    test_list_users()
    
    # Probar creación de usuario
    test_create_user()
    
    # Listar usuarios después de la prueba
    test_list_users()

if __name__ == "__main__":
    main()
