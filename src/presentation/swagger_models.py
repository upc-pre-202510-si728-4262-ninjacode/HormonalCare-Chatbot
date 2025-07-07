from flask_restx import fields

def create_swagger_models(api):
    """Crear modelos de Swagger para la documentación de la API"""
    
    # Modelo para crear usuario
    user_input_model = api.model('UserInput', {
        'name': fields.String(required=True, description='Nombre completo del usuario', example='Juan Pérez'),
        'age': fields.Integer(required=True, description='Edad del usuario', example=35),
        'gender': fields.String(required=True, description='Género del usuario', enum=['male', 'female', 'masculino', 'femenino'], example='male')
    })
    
    # Modelo de respuesta de usuario
    user_response_model = api.model('UserResponse', {
        'id': fields.String(description='ID único del usuario', example='123e4567-e89b-12d3-a456-426614174000'),
        'name': fields.String(description='Nombre del usuario', example='Juan Pérez'),
        'age': fields.Integer(description='Edad del usuario', example=35),
        'gender': fields.String(description='Género del usuario', example='male'),
        'created_at': fields.String(description='Fecha de creación', example='2025-01-15T10:30:00.000Z')
    })
    
    # Modelo para análisis de examen de sangre
    blood_test_input_model = api.model('BloodTestInput', {
        'user_id': fields.String(required=True, description='ID del usuario', example='123e4567-e89b-12d3-a456-426614174000'),
        'glucose': fields.Float(required=True, description='Glucosa en mg/dL', example=95.0),
        'cholesterol': fields.Float(required=True, description='Colesterol total en mg/dL', example=180.0),
        'hdl_cholesterol': fields.Float(description='HDL (colesterol bueno) en mg/dL', example=55.0),
        'ldl_cholesterol': fields.Float(description='LDL (colesterol malo) en mg/dL', example=110.0),
        'triglycerides': fields.Float(description='Triglicéridos en mg/dL', example=120.0),
        'hemoglobin': fields.Float(description='Hemoglobina en g/dL', example=13.5),
        'hematocrit': fields.Float(description='Hematocrito en %', example=40.0),
        'white_blood_cells': fields.Float(description='Glóbulos blancos por μL', example=6500.0),
        'red_blood_cells': fields.Float(description='Glóbulos rojos en millones/μL', example=4.2),
        'platelets': fields.Float(description='Plaquetas por μL', example=280000.0),
        'creatinine': fields.Float(description='Creatinina en mg/dL', example=0.9),
        'urea': fields.Float(description='Urea en mg/dL', example=30.0),
        'test_date': fields.String(description='Fecha del examen (ISO)', example='2025-01-15T08:00:00.000Z')
    })
    
    # Modelo de recomendación
    recommendation_model = api.model('Recommendation', {
        'type': fields.String(description='Tipo de recomendación', enum=['dietary', 'exercise', 'medication', 'medical_consultation', 'lifestyle']),
        'title': fields.String(description='Título de la recomendación', example='Dieta baja en carbohidratos'),
        'description': fields.String(description='Descripción detallada', example='Reducir el consumo de azúcares y carbohidratos refinados'),
        'priority': fields.Integer(description='Prioridad (1-5)', example=4)
    })
    
    # Modelo de análisis de examen
    blood_analysis_model = api.model('BloodAnalysis', {
        'overall_risk': fields.String(description='Riesgo general', enum=['low', 'moderate', 'high', 'critical'], example='moderate'),
        'glucose_status': fields.String(description='Estado de la glucosa', example='Normal - Nivel de glucosa en ayunas normal'),
        'cholesterol_status': fields.String(description='Estado del colesterol', example='Normal - Perfil lipídico dentro de rangos normales'),
        'kidney_function_status': fields.String(description='Estado de función renal', example='Normal - Función renal dentro de parámetros normales'),
        'blood_count_status': fields.String(description='Estado del hemograma', example='Normal - Hemograma completo dentro de rangos normales'),
        'recommendations': fields.List(fields.Nested(recommendation_model), description='Lista de recomendaciones'),
        'needs_doctor_consultation': fields.Boolean(description='Requiere consulta médica', example=False),
        'risk_factors': fields.List(fields.String, description='Factores de riesgo identificados', example=['Edad de riesgo cardiovascular'])
    })
    
    # Modelo de respuesta de análisis
    blood_test_response_model = api.model('BloodTestResponse', {
        'blood_test_id': fields.String(description='ID del examen', example='123e4567-e89b-12d3-a456-426614174001'),
        'conversation_id': fields.String(description='ID de la conversación', example='123e4567-e89b-12d3-a456-426614174002'),
        'analysis': fields.Nested(blood_analysis_model, description='Análisis del examen'),
        'ai_explanation': fields.String(description='Explicación generada por IA', example='Sus resultados muestran niveles normales en la mayoría de parámetros...')
    })
    
    # Modelo para mensaje de chat
    chat_message_input_model = api.model('ChatMessageInput', {
        'message': fields.String(required=True, description='Mensaje del usuario', example='¿Mis resultados están normales?')
    })
    
    # Modelo de respuesta de chat
    chat_response_model = api.model('ChatResponse', {
        'user_message': fields.String(description='Mensaje del usuario', example='¿Mis resultados están normales?'),
        'assistant_response': fields.String(description='Respuesta del asistente', example='Según sus resultados, la mayoría de sus valores están dentro del rango normal...'),
        'timestamp': fields.String(description='Timestamp del mensaje', example='2025-01-15T10:35:00.000Z')
    })
    
    # Modelo de examen en historial
    blood_test_history_model = api.model('BloodTestHistory', {
        'id': fields.String(description='ID del examen'),
        'glucose': fields.Float(description='Glucosa'),
        'cholesterol': fields.Float(description='Colesterol'),
        'test_date': fields.String(description='Fecha del examen'),
        'created_at': fields.String(description='Fecha de creación')
    })
    
    # Modelo de conversación en historial
    conversation_history_model = api.model('ConversationHistory', {
        'id': fields.String(description='ID de la conversación'),
        'blood_test_id': fields.String(description='ID del examen asociado'),
        'created_at': fields.String(description='Fecha de creación'),
        'message_count': fields.Integer(description='Número de mensajes')
    })
    
    # Modelo de historial de usuario
    user_history_model = api.model('UserHistory', {
        'user': fields.Nested(user_response_model, description='Información del usuario'),
        'blood_tests': fields.List(fields.Nested(blood_test_history_model), description='Historial de exámenes'),
        'conversations': fields.List(fields.Nested(conversation_history_model), description='Historial de conversaciones')
    })
    
    # Modelos de respuesta estándar
    success_response_model = api.model('SuccessResponse', {
        'success': fields.Boolean(description='Indica si la operación fue exitosa', example=True),
        'message': fields.String(description='Mensaje descriptivo', example='Operación completada exitosamente'),
        'data': fields.Raw(description='Datos de respuesta')
    })
    
    error_response_model = api.model('ErrorResponse', {
        'error': fields.String(description='Mensaje de error', example='Campo requerido: name')
    })
    
    health_response_model = api.model('HealthResponse', {
        'status': fields.String(description='Estado de la API', example='healthy'),
        'message': fields.String(description='Mensaje de estado', example='Medical Chatbot API is running')
    })
    
    return {
        'user_input': user_input_model,
        'user_response': user_response_model,
        'blood_test_input': blood_test_input_model,
        'blood_test_response': blood_test_response_model,
        'blood_analysis': blood_analysis_model,
        'recommendation': recommendation_model,
        'chat_message_input': chat_message_input_model,
        'chat_response': chat_response_model,
        'user_history': user_history_model,
        'blood_test_history': blood_test_history_model,
        'conversation_history': conversation_history_model,
        'success_response': success_response_model,
        'error_response': error_response_model,
        'health_response': health_response_model
    }
