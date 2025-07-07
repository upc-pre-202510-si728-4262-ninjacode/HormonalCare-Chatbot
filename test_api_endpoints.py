#!/usr/bin/env python3
"""
Script para probar el endpoint de creación de usuarios
"""

import requests
import json

def test_create_user_endpoint():
    """Probar el endpoint POST /api/users"""
    
    print("🧪 Probando endpoint POST /api/users")
    print("=" * 40)
    
    # Datos del usuario de prueba
    user_data = {
        "name": "Juan Pérez",
        "age": 35,
        "gender": "masculino"
    }
    
    try:
        # Hacer la petición POST
        url = "http://localhost:5000/api/users"
        response = requests.post(url, json=user_data)
        
        print(f"📡 URL: {url}")
        print(f"📤 Datos enviados: {json.dumps(user_data, indent=2)}")
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 201:
            response_data = response.json()
            print("✅ Usuario creado exitosamente!")
            print(f"   ID: {response_data.get('data', {}).get('id')}")
            return response_data.get('data', {}).get('id')
        else:
            print("❌ Error al crear usuario")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al servidor. ¿Está ejecutándose en http://localhost:5000?")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def test_get_user_history(user_id):
    """Probar el endpoint GET /api/users/{user_id}/history"""
    
    if not user_id:
        return
        
    print(f"\n🧪 Probando endpoint GET /api/users/{user_id}/history")
    print("=" * 50)
    
    try:
        url = f"http://localhost:5000/api/users/{user_id}/history"
        response = requests.get(url)
        
        print(f"📡 URL: {url}")
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Historial obtenido exitosamente!")
        else:
            print("❌ Error al obtener historial")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Función principal"""
    print("🏥 Test de API - Medical Chatbot")
    print("=" * 35)
    
    print("⚠️  Asegúrate de que el servidor esté ejecutándose:")
    print("   python app.py")
    print()
    
    # Probar creación de usuario
    user_id = test_create_user_endpoint()
    
    # Probar obtener historial
    test_get_user_history(user_id)

if __name__ == "__main__":
    main()
