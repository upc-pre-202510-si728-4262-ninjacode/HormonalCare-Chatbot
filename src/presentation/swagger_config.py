"""
Configuración personalizada para Swagger UI
"""

SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

# Información adicional para la documentación
API_INFO = {
    "title": "Medical Chatbot API",
    "version": "1.0.0",
    "description": """
## 🏥 API para Chatbot Médico

Esta API permite analizar exámenes de sangre usando inteligencia artificial y proporciona 
un chatbot especializado para interpretar resultados médicos.

### Características principales:
- **Análisis inteligente** de exámenes de sangre
- **Evaluación de riesgos** médicos
- **Recomendaciones personalizadas**
- **Chat interactivo** con IA médica
- **Historial** de conversaciones y exámenes

### Flujo típico de uso:
1. Crear un usuario con `POST /users`
2. Analizar examen de sangre con `POST /chat/analyze`
3. Interactuar con el chatbot usando `POST /chat/{conversation_id}/message`
4. Consultar historial con `GET /users/{user_id}/history`

### Valores de referencia comunes:
- **Glucosa**: 70-100 mg/dL (normal)
- **Colesterol total**: <200 mg/dL (deseable)
- **HDL**: >40 mg/dL (hombres), >50 mg/dL (mujeres)
- **LDL**: <100 mg/dL (óptimo)
- **Triglicéridos**: <150 mg/dL (normal)

⚠️ **Importante**: Esta API es solo para fines informativos y no reemplaza 
el consejo médico profesional.
    """,
    "contact": {
        "name": "Equipo de Desarrollo",
        "email": "desarrollo@chatbot-medico.com"
    },
    "license": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
}

# Configuración de modelos de ejemplo
EXAMPLE_DATA = {
    "user_example": {
        "name": "María García",
        "age": 45,
        "gender": "female"
    },
    "blood_test_example": {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "glucose": 95.0,
        "cholesterol": 180.0,
        "hdl_cholesterol": 55.0,
        "ldl_cholesterol": 110.0,
        "triglycerides": 120.0,
        "hemoglobin": 13.5,
        "hematocrit": 40.0,
        "white_blood_cells": 6500.0,
        "red_blood_cells": 4.2,
        "platelets": 280000.0,
        "creatinine": 0.9,
        "urea": 30.0,
        "test_date": "2025-01-15T08:00:00.000Z"
    },
    "chat_message_example": {
        "message": "¿Mis resultados están dentro del rango normal? ¿Debo preocuparme por algo?"
    }
}
