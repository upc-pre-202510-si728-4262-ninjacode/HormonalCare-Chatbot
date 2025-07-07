#!/usr/bin/env python3
"""
Script para limpiar la base de datos del Medical Chatbot
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
from src.infrastructure.database import db, UserModel, BloodTestModel, ChatConversationModel, ChatMessageModel
from flask import Flask

# Cargar variables de entorno
load_dotenv()

def create_app():
    """Crear aplicación Flask para acceder a la base de datos"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///medical_chatbot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def clear_database():
    """Limpiar completamente la base de datos"""
    app = create_app()
    
    with app.app_context():
        print("🗑️  Limpiando base de datos del Medical Chatbot...")
        print("=" * 50)
        
        try:
            # Contar registros antes de limpiar
            users_count = UserModel.query.count()
            blood_tests_count = BloodTestModel.query.count()
            conversations_count = ChatConversationModel.query.count()
            messages_count = ChatMessageModel.query.count()
            
            print(f"📊 Registros actuales:")
            print(f"   - Usuarios: {users_count}")
            print(f"   - Exámenes de sangre: {blood_tests_count}")
            print(f"   - Conversaciones: {conversations_count}")
            print(f"   - Mensajes: {messages_count}")
            print()
            
            if users_count == 0 and blood_tests_count == 0 and conversations_count == 0 and messages_count == 0:
                print("✅ La base de datos ya está vacía.")
                return
            
            # Confirmar antes de proceder
            response = input("⚠️  ¿Estás seguro de que quieres eliminar TODOS los datos? (escribe 'confirmar'): ")
            if response.lower() != 'confirmar':
                print("❌ Operación cancelada.")
                return
            
            print("\n🔄 Eliminando datos...")
            
            # Eliminar en orden correcto (respetando foreign keys)
            print("   - Eliminando mensajes...")
            ChatMessageModel.query.delete()
            
            print("   - Eliminando conversaciones...")
            ChatConversationModel.query.delete()
            
            print("   - Eliminando exámenes de sangre...")
            BloodTestModel.query.delete()
            
            print("   - Eliminando usuarios...")
            UserModel.query.delete()
            
            # Confirmar cambios
            db.session.commit()
            
            print("\n✅ Base de datos limpiada exitosamente!")
            print(f"🕒 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"\n❌ Error al limpiar la base de datos: {e}")
            db.session.rollback()
            return False
    
    return True

def reset_database():
    """Resetear la base de datos (eliminar y recrear tablas)"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Reseteando base de datos del Medical Chatbot...")
        print("=" * 50)
        
        try:
            # Confirmar antes de proceder
            response = input("⚠️  ¿Estás seguro de que quieres RESETEAR completamente la BD? (escribe 'resetear'): ")
            if response.lower() != 'resetear':
                print("❌ Operación cancelada.")
                return
            
            print("\n🗑️  Eliminando todas las tablas...")
            db.drop_all()
            
            print("🏗️  Recreando tablas...")
            db.create_all()
            
            print("\n✅ Base de datos reseteada exitosamente!")
            print("🆕 Todas las tablas han sido recreadas vacías.")
            print(f"🕒 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"\n❌ Error al resetear la base de datos: {e}")
            return False
    
    return True

def show_stats():
    """Mostrar estadísticas de la base de datos"""
    app = create_app()
    
    with app.app_context():
        print("📊 Estadísticas de la base de datos")
        print("=" * 35)
        
        try:
            users_count = UserModel.query.count()
            blood_tests_count = BloodTestModel.query.count()
            conversations_count = ChatConversationModel.query.count()
            messages_count = ChatMessageModel.query.count()
            
            print(f"👥 Usuarios: {users_count}")
            print(f"🩸 Exámenes de sangre: {blood_tests_count}")
            print(f"💬 Conversaciones: {conversations_count}")
            print(f"📝 Mensajes: {messages_count}")
            
            if users_count > 0:
                print("\n📋 Últimos usuarios registrados:")
                recent_users = UserModel.query.order_by(UserModel.created_at.desc()).limit(5).all()
                for user in recent_users:
                    print(f"   - {user.name} ({user.age} años, {user.gender}) - {user.created_at.strftime('%Y-%m-%d %H:%M')}")
            
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")

def main():
    """Función principal del script"""
    print("🏥 Medical Chatbot - Administrador de Base de Datos")
    print("=" * 55)
    print()
    print("Opciones disponibles:")
    print("1. Ver estadísticas")
    print("2. Limpiar datos (mantener estructura)")
    print("3. Resetear base de datos (eliminar y recrear tablas)")
    print("4. Salir")
    print()
    
    while True:
        try:
            choice = input("Selecciona una opción (1-4): ").strip()
            print()
            
            if choice == '1':
                show_stats()
            elif choice == '2':
                clear_database()
            elif choice == '3':
                reset_database()
            elif choice == '4':
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Por favor selecciona 1, 2, 3 o 4.")
            
            print("\n" + "-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Operación cancelada por el usuario.")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
