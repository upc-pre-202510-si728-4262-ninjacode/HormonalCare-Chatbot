#!/usr/bin/env python3
"""
Script para migrar datos de SQLite a MySQL
"""

import os
import sys
import sqlite3
import pymysql
import json
from datetime import datetime
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def connect_sqlite():
    """Conectar a la base de datos SQLite"""
    db_file = Path('medical_chatbot.db')
    if not db_file.exists():
        print("❌ Archivo SQLite no encontrado")
        return None
    
    try:
        conn = sqlite3.connect(str(db_file))
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        print("✅ Conectado a SQLite")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a SQLite: {e}")
        return None

def connect_mysql():
    """Conectar a la base de datos MySQL"""
    try:
        conn = pymysql.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'root'),
            database=os.getenv('MYSQL_DATABASE', 'chatbot'),
            charset='utf8mb4',
            autocommit=True
        )
        print("✅ Conectado a MySQL")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return None

def migrate_table(sqlite_conn, mysql_conn, table_name, columns):
    """Migrar una tabla específica"""
    print(f"📋 Migrando tabla: {table_name}")
    
    try:
        # Leer datos de SQLite
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"   ℹ️  Tabla {table_name} está vacía")
            return True
        
        # Preparar consulta de inserción para MySQL
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Insertar datos en MySQL
        mysql_cursor = mysql_conn.cursor()
        
        migrated_count = 0
        for row in rows:
            try:
                values = [row[col] for col in columns]
                mysql_cursor.execute(insert_query, values)
                migrated_count += 1
            except Exception as e:
                print(f"   ⚠️  Error migrando registro: {e}")
        
        print(f"   ✅ {migrated_count} registros migrados")
        return True
        
    except Exception as e:
        print(f"   ❌ Error migrando tabla {table_name}: {e}")
        return False

def clear_mysql_tables(mysql_conn):
    """Limpiar tablas MySQL antes de migrar"""
    print("🗑️  Limpiando tablas MySQL...")
    
    try:
        cursor = mysql_conn.cursor()
        
        # Deshabilitar foreign key checks temporalmente
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Limpiar tablas en orden
        tables = ['chat_messages', 'chat_conversations', 'blood_tests', 'users']
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"   ✅ Tabla {table} limpiada")
        
        # Rehabilitar foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        return True
    except Exception as e:
        print(f"❌ Error limpiando tablas: {e}")
        return False

def migrate_data():
    """Migrar todos los datos"""
    print("🔄 Iniciando migración de SQLite a MySQL")
    print("=" * 50)
    
    # Conectar a ambas bases de datos
    sqlite_conn = connect_sqlite()
    if not sqlite_conn:
        return False
    
    mysql_conn = connect_mysql()
    if not mysql_conn:
        sqlite_conn.close()
        return False
    
    try:
        # Confirmar antes de proceder
        response = input("⚠️  ¿Estás seguro de que quieres migrar los datos? (escribe 'migrar'): ")
        if response.lower() != 'migrar':
            print("❌ Migración cancelada.")
            return False
        
        # Limpiar tablas MySQL
        if not clear_mysql_tables(mysql_conn):
            return False
        
        print("\n📋 Migrando datos...")
        
        # Definir estructura de tablas
        tables_structure = {
            'users': ['id', 'name', 'age', 'gender', 'created_at'],
            'blood_tests': ['id', 'user_id', 'glucose', 'cholesterol', 'hdl_cholesterol', 
                           'ldl_cholesterol', 'triglycerides', 'hemoglobin', 'hematocrit',
                           'white_blood_cells', 'red_blood_cells', 'platelets', 'creatinine',
                           'urea', 'test_date', 'created_at'],
            'chat_conversations': ['id', 'user_id', 'blood_test_id', 'created_at'],
            'chat_messages': ['id', 'conversation_id', 'content', 'sender', 'timestamp']
        }
        
        # Migrar cada tabla
        success = True
        for table_name, columns in tables_structure.items():
            if not migrate_table(sqlite_conn, mysql_conn, table_name, columns):
                success = False
        
        if success:
            print("\n🎉 ¡Migración completada exitosamente!")
            print(f"🕒 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("\n⚠️  Migración completada con errores")
        
        return success
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False
    finally:
        sqlite_conn.close()
        mysql_conn.close()

def show_comparison():
    """Mostrar comparación entre SQLite y MySQL"""
    print("📊 Comparación de datos SQLite vs MySQL")
    print("=" * 45)
    
    # Conectar a SQLite
    sqlite_conn = connect_sqlite()
    if sqlite_conn:
        print("\n🗄️  Datos en SQLite:")
        try:
            cursor = sqlite_conn.cursor()
            tables = ['users', 'blood_tests', 'chat_conversations', 'chat_messages']
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   {table}: {count} registros")
                except:
                    print(f"   {table}: tabla no existe")
        except Exception as e:
            print(f"   Error: {e}")
        finally:
            sqlite_conn.close()
    
    # Conectar a MySQL
    mysql_conn = connect_mysql()
    if mysql_conn:
        print("\n🐬 Datos en MySQL:")
        try:
            cursor = mysql_conn.cursor()
            tables = ['users', 'blood_tests', 'chat_conversations', 'chat_messages']
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   {table}: {count} registros")
                except:
                    print(f"   {table}: tabla no existe")
        except Exception as e:
            print(f"   Error: {e}")
        finally:
            mysql_conn.close()

def main():
    """Función principal"""
    print("🏥 Medical Chatbot - Migración SQLite → MySQL")
    print("=" * 50)
    print()
    print("Opciones disponibles:")
    print("1. Ver comparación de datos")
    print("2. Migrar datos de SQLite a MySQL")
    print("3. Salir")
    print()
    
    while True:
        try:
            choice = input("Selecciona una opción (1-3): ").strip()
            print()
            
            if choice == '1':
                show_comparison()
            elif choice == '2':
                migrate_data()
            elif choice == '3':
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Por favor selecciona 1, 2 o 3.")
            
            print("\n" + "-" * 50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Operación cancelada por el usuario.")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
