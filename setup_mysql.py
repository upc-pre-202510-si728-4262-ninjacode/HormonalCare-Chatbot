#!/usr/bin/env python3
"""
Script para configurar la base de datos MySQL para el chatbot médico.
Verifica la conexión, crea la base de datos si no existe, y configura las tablas.
"""

import os
import pymysql
from dotenv import load_dotenv
from flask import Flask
from src.infrastructure.database import db

# Cargar variables de entorno
load_dotenv()

def check_mysql_connection():
    """Verificar la conexión a MySQL"""
    print("🔍 Verificando conexión a MySQL...")
    
    try:
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'root')
        )
        print("✅ Conexión a MySQL exitosa")
        return connection
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        print("\n📋 Verifica que:")
        print("1. MySQL esté ejecutándose")
        print("2. Las credenciales en .env sean correctas")
        print("3. El usuario tenga permisos suficientes")
        return None

def create_database_if_not_exists(connection):
    """Crear la base de datos si no existe"""
    database_name = os.getenv('MYSQL_DATABASE', 'chatbot')
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"✅ Base de datos '{database_name}' verificada/creada")
        return True
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def create_tables():
    """Crear las tablas usando SQLAlchemy"""
    print("🏗️ Creando tablas...")
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    try:
        with app.app_context():
            db.create_all()
        print("✅ Tablas creadas exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def verify_tables():
    """Verificar que las tablas existan"""
    print("🔍 Verificando tablas...")
    
    try:
        connection = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'root'),
            database=os.getenv('MYSQL_DATABASE', 'chatbot')
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            expected_tables = ['users', 'blood_tests', 'chat_conversations', 'chat_messages']
            found_tables = [table[0] for table in tables]
            
            print(f"📊 Tablas encontradas: {found_tables}")
            
            missing_tables = [table for table in expected_tables if table not in found_tables]
            if missing_tables:
                print(f"⚠️ Tablas faltantes: {missing_tables}")
                return False
            else:
                print("✅ Todas las tablas están presentes")
                return True
                
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

def main():
    """Función principal"""
    print("🏥 Configuración de Base de Datos - Medical Chatbot")
    print("=" * 50)
    
    # 1. Verificar conexión a MySQL
    connection = check_mysql_connection()
    if not connection:
        return
    
    # 2. Crear base de datos si no existe
    if not create_database_if_not_exists(connection):
        return
    
    connection.close()
    
    # 3. Crear tablas
    if not create_tables():
        return
    
    # 4. Verificar tablas
    if not verify_tables():
        return
    
    print("\n🎉 ¡Configuración completada exitosamente!")
    print("📖 Puedes iniciar la aplicación con: python app.py")

if __name__ == "__main__":
    main()
