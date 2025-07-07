"""
Script de ejemplo para probar la API del chatbot médico

Alternativamente, puedes usar la interfaz de Swagger en:
http://localhost:5000/docs/
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000/api"

def test_create_user():
    """Crear un usuario de prueba"""
    user_data = {
        "name": "Juan Pérez",
        "age": 35,
        "gender": "male"
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print("=== Crear Usuario ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        return response.json()['data']['id']
    return None

def test_analyze_blood_test(user_id):
    """Analizar un examen de sangre"""
    blood_test_data = {
        "user_id": user_id,
        "glucose": 120,  # Ligeramente elevado
        "cholesterol": 220,  # Elevado
        "hdl_cholesterol": 35,  # Bajo
        "ldl_cholesterol": 140,  # Elevado
        "triglycerides": 180,  # Elevado
        "hemoglobin": 14.0,  # Normal
        "hematocrit": 42.0,  # Normal
        "white_blood_cells": 7500,  # Normal
        "red_blood_cells": 4.5,  # Normal
        "platelets": 250000,  # Normal
        "creatinine": 1.0,  # Normal
        "urea": 25,  # Normal
        "test_date": datetime.now().isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/chat/analyze", json=blood_test_data)
    print("\n=== Analizar Examen de Sangre ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        return response.json()['data']['conversation_id']
    return None

def test_chat_message(conversation_id):
    """Enviar mensaje al chatbot"""
    messages = [
        "¿Qué tan grave son mis resultados?",
        "¿Debo contactar a mi doctor inmediatamente?",
        "¿Qué puedo hacer para mejorar mi colesterol?",
        "¿Es normal que mi glucosa esté un poco alta?"
    ]
    
    for message in messages:
        message_data = {"message": message}
        response = requests.post(f"{BASE_URL}/chat/{conversation_id}/message", json=message_data)
        
        print(f"\n=== Mensaje: {message} ===")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()['data']
            print(f"Usuario: {data['user_message']}")
            print(f"Asistente: {data['assistant_response']}")
        else:
            print(f"Error: {response.json()}")

def test_user_history(user_id):
    """Obtener historial del usuario"""
    response = requests.get(f"{BASE_URL}/users/{user_id}/history")
    print(f"\n=== Historial del Usuario ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_health_check():
    """Verificar que la API esté funcionando"""
    response = requests.get(f"{BASE_URL}/health")
    print("=== Health Check ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    print("🏥 Probando API del Chatbot Médico\n")
    
    # Verificar que la API esté funcionando
    try:
        test_health_check()
        
        # Crear usuario
        user_id = test_create_user()
        if not user_id:
            print("❌ Error al crear usuario")
            exit(1)
        
        # Analizar examen de sangre
        conversation_id = test_analyze_blood_test(user_id)
        if not conversation_id:
            print("❌ Error al analizar examen")
            exit(1)
        
        # Chatear con el bot
        test_chat_message(conversation_id)
        
        # Obtener historial
        test_user_history(user_id)
        
        print("\n✅ Todas las pruebas completadas exitosamente!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la API. ¿Está ejecutándose el servidor?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
