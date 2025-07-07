# API Documentation - Medical Chatbot

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Health Check
**GET** `/health`

Verifica que la API esté funcionando.

**Response:**
```json
{
  "status": "healthy",
  "message": "Medical Chatbot API is running"
}
```

### 2. Crear Usuario
**POST** `/users`

Crea un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "name": "string",
  "age": "number",
  "gender": "string" // "male", "female", "masculino", "femenino"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "id": "uuid",
    "name": "string",
    "age": "number",
    "gender": "string",
    "created_at": "iso_date"
  }
}
```

### 3. Analizar Examen de Sangre
**POST** `/chat/analyze`

Analiza un examen de sangre y crea una conversación inicial con el chatbot.

**Request Body:**
```json
{
  "user_id": "uuid",
  "glucose": "number",
  "cholesterol": "number",
  "hdl_cholesterol": "number",
  "ldl_cholesterol": "number",
  "triglycerides": "number",
  "hemoglobin": "number",
  "hematocrit": "number",
  "white_blood_cells": "number",
  "red_blood_cells": "number",
  "platelets": "number",
  "creatinine": "number",
  "urea": "number",
  "test_date": "iso_date" // opcional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Examen analizado exitosamente",
  "data": {
    "blood_test_id": "uuid",
    "conversation_id": "uuid",
    "analysis": {
      "overall_risk": "low|moderate|high|critical",
      "glucose_status": "string",
      "cholesterol_status": "string",
      "kidney_function_status": "string",
      "blood_count_status": "string",
      "recommendations": [
        {
          "type": "dietary|exercise|medication|medical_consultation|lifestyle",
          "title": "string",
          "description": "string",
          "priority": "number"
        }
      ],
      "needs_doctor_consultation": "boolean",
      "risk_factors": ["string"]
    },
    "ai_explanation": "string"
  }
}
```

### 4. Enviar Mensaje al Chat
**POST** `/chat/{conversation_id}/message`

Envía un mensaje al chatbot en una conversación existente.

**Request Body:**
```json
{
  "message": "string"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_message": "string",
    "assistant_response": "string",
    "timestamp": "iso_date"
  }
}
```

### 5. Obtener Historial de Usuario
**GET** `/users/{user_id}/history`

Obtiene el historial completo de un usuario: exámenes y conversaciones.

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "uuid",
      "name": "string",
      "age": "number",
      "gender": "string"
    },
    "blood_tests": [
      {
        "id": "uuid",
        "glucose": "number",
        "cholesterol": "number",
        "test_date": "iso_date",
        "created_at": "iso_date"
      }
    ],
    "conversations": [
      {
        "id": "uuid",
        "blood_test_id": "uuid",
        "created_at": "iso_date",
        "message_count": "number"
      }
    ]
  }
}
```

## Códigos de Error

- **400**: Bad Request - Datos inválidos o faltantes
- **404**: Not Found - Recurso no encontrado
- **405**: Method Not Allowed - Método HTTP no permitido
- **500**: Internal Server Error - Error del servidor

## Ejemplos de Uso

### Ejemplo 1: Flujo Completo

```bash
# 1. Crear usuario
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "María García",
    "age": 45,
    "gender": "female"
  }'

# 2. Analizar examen (usar el user_id del paso anterior)
curl -X POST http://localhost:5000/api/chat/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-uuid-here",
    "glucose": 95,
    "cholesterol": 180,
    "hdl_cholesterol": 55,
    "ldl_cholesterol": 110,
    "triglycerides": 120,
    "hemoglobin": 13.5,
    "hematocrit": 40,
    "white_blood_cells": 6500,
    "red_blood_cells": 4.2,
    "platelets": 280000,
    "creatinine": 0.9,
    "urea": 30
  }'

# 3. Chatear (usar conversation_id del paso anterior)
curl -X POST http://localhost:5000/api/chat/conversation-uuid-here/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Mis resultados están normales?"
  }'
```

### Ejemplo 2: Valores de Referencia

**Glucosa:**
- Normal: 70-100 mg/dL
- Prediabetes: 100-125 mg/dL
- Diabetes: >125 mg/dL

**Colesterol Total:**
- Deseable: <200 mg/dL
- Límite alto: 200-239 mg/dL
- Alto: ≥240 mg/dL

**HDL (Colesterol Bueno):**
- Hombres: >40 mg/dL
- Mujeres: >50 mg/dL

**LDL (Colesterol Malo):**
- Óptimo: <100 mg/dL
- Casi óptimo: 100-129 mg/dL
- Límite alto: 130-159 mg/dL
- Alto: 160-189 mg/dL
- Muy alto: ≥190 mg/dL

**Triglicéridos:**
- Normal: <150 mg/dL
- Límite alto: 150-199 mg/dL
- Alto: 200-499 mg/dL
- Muy alto: ≥500 mg/dL
