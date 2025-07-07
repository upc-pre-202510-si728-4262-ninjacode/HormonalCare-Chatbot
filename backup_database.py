#!/usr/bin/env python3
"""
Script para hacer backup de la base de datos del Medical Chatbot
"""

import os
import sys
import shutil
import json
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

def backup_database():
    """Crear backup de la base de datos"""
    app = create_app()
    
    with app.app_context():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = Path('backups')
        backup_dir.mkdir(exist_ok=True)
        
        print(f"💾 Creando backup de la base de datos...")
        print(f"📅 Timestamp: {timestamp}")
        print("=" * 50)
        
        try:
            # Para MySQL, creamos un dump en JSON
            database_url = os.getenv('DATABASE_URL', '')
            if 'mysql' in database_url:
                print("🐬 Detectada base de datos MySQL - creando backup JSON...")
            else:
                # Backup del archivo SQLite
                db_file = Path('medical_chatbot.db')
                if db_file.exists():
                    backup_file = backup_dir / f'medical_chatbot_backup_{timestamp}.db'
                    shutil.copy2(db_file, backup_file)
                    print(f"✅ Archivo DB copiado a: {backup_file}")
            
            # Backup en formato JSON
            json_backup = backup_dir / f'medical_chatbot_data_{timestamp}.json'
            
            # Exportar datos a JSON
            backup_data = {
                'timestamp': timestamp,
                'users': [],
                'blood_tests': [],
                'conversations': [],
                'messages': []
            }
            
            # Exportar usuarios
            users = UserModel.query.all()
            for user in users:
                backup_data['users'].append({
                    'id': str(user.id),
                    'name': user.name,
                    'age': user.age,
                    'gender': user.gender,
                    'created_at': user.created_at.isoformat()
                })
            
            # Exportar exámenes
            blood_tests = BloodTestModel.query.all()
            for test in blood_tests:
                backup_data['blood_tests'].append({
                    'id': str(test.id),
                    'user_id': str(test.user_id),
                    'glucose': test.glucose,
                    'cholesterol': test.cholesterol,
                    'hdl_cholesterol': test.hdl_cholesterol,
                    'ldl_cholesterol': test.ldl_cholesterol,
                    'triglycerides': test.triglycerides,
                    'hemoglobin': test.hemoglobin,
                    'hematocrit': test.hematocrit,
                    'white_blood_cells': test.white_blood_cells,
                    'red_blood_cells': test.red_blood_cells,
                    'platelets': test.platelets,
                    'creatinine': test.creatinine,
                    'urea': test.urea,
                    'test_date': test.test_date.isoformat(),
                    'created_at': test.created_at.isoformat()
                })
            
            # Exportar conversaciones
            conversations = ChatConversationModel.query.all()
            for conv in conversations:
                backup_data['conversations'].append({
                    'id': str(conv.id),
                    'user_id': str(conv.user_id),
                    'blood_test_id': str(conv.blood_test_id) if conv.blood_test_id else None,
                    'created_at': conv.created_at.isoformat()
                })
            
            # Exportar mensajes
            messages = ChatMessageModel.query.all()
            for msg in messages:
                backup_data['messages'].append({
                    'id': str(msg.id),
                    'conversation_id': str(msg.conversation_id),
                    'content': msg.content,
                    'sender': msg.sender,
                    'timestamp': msg.timestamp.isoformat()
                })
            
            # Guardar JSON
            with open(json_backup, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos exportados a JSON: {json_backup}")
            
            # Estadísticas del backup
            print(f"\n📊 Estadísticas del backup:")
            print(f"   - Usuarios: {len(backup_data['users'])}")
            print(f"   - Exámenes: {len(backup_data['blood_tests'])}")
            print(f"   - Conversaciones: {len(backup_data['conversations'])}")
            print(f"   - Mensajes: {len(backup_data['messages'])}")
            
            print(f"\n✅ Backup completado exitosamente!")
            
        except Exception as e:
            print(f"❌ Error al crear backup: {e}")
            return False
    
    return True

if __name__ == "__main__":
    backup_database()
