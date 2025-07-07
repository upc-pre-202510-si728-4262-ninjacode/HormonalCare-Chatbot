from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, Namespace
from .swagger_models import create_swagger_models
from ..application.use_cases import (
    CreateUserUseCase, 
    AnalyzeBloodTestUseCase, 
    ChatWithUserUseCase, 
    GetUserHistoryUseCase
)

def create_api(app: Flask, user_controller_factory, chat_controller_factory):
    """Crear la API con Swagger/OpenAPI"""
    
    # Configurar Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='Medical Chatbot API',
        description='API REST para chatbot médico que analiza exámenes de sangre con IA',
        doc='/docs/',  # Swagger UI estará disponible en /docs/
        prefix='/api'
    )
    
    # Crear modelos de Swagger
    models = create_swagger_models(api)
    
    # Crear namespaces
    users_ns = Namespace('users', description='Operaciones de usuarios')
    chat_ns = Namespace('chat', description='Operaciones de chat y análisis médico')
    health_ns = Namespace('health', description='Estado de la API')
    
    # Registrar namespaces
    api.add_namespace(users_ns)
    api.add_namespace(chat_ns)
    api.add_namespace(health_ns)
    
    # Obtener controladores
    user_controller = user_controller_factory()
    chat_controller = chat_controller_factory()
    
    # === ENDPOINTS DE USUARIOS ===
    
    @users_ns.route('')
    class UserList(Resource):
        @users_ns.doc('create_user')
        @users_ns.expect(models['user_input'])
        @users_ns.marshal_with(models['success_response'], code=201)
        @users_ns.response(400, 'Datos inválidos', models['error_response'])
        def post(self):
            """Crear un nuevo usuario"""
            try:
                data = request.get_json()
                
                # Validar datos requeridos
                required_fields = ['name', 'age', 'gender']
                for field in required_fields:
                    if field not in data:
                        return {'error': f'Campo requerido: {field}'}, 400
                
                # Validar tipos de datos
                if not isinstance(data['age'], (int, float)) or data['age'] <= 0:
                    return {'error': 'La edad debe ser un número positivo'}, 400
                
                if data['gender'].lower() not in ['male', 'female', 'masculino', 'femenino']:
                    return {'error': 'Género debe ser male/female o masculino/femenino'}, 400
                
                # Crear usuario
                result = user_controller.create_user_logic(data)
                
                return {
                    'success': True,
                    'message': 'Usuario creado exitosamente',
                    'data': result
                }, 201
                
            except ValueError as e:
                return {'error': str(e)}, 400
            except Exception as e:
                return {'error': 'Error interno del servidor'}, 500
    
    @users_ns.route('/<string:user_id>/history')
    class UserHistory(Resource):
        @users_ns.doc('get_user_history')
        @users_ns.marshal_with(models['success_response'])
        @users_ns.response(400, 'ID de usuario inválido', models['error_response'])
        @users_ns.response(404, 'Usuario no encontrado', models['error_response'])
        def get(self, user_id):
            """Obtener historial completo de un usuario"""
            try:
                # Validar user_id (ya no necesita ser UUID)
                if not isinstance(user_id, str) or not user_id.strip():
                    return {'error': 'user_id debe ser una cadena válida'}, 400
                    
                result = user_controller.get_user_history_logic(user_id)
                
                return {
                    'success': True,
                    'data': result
                }, 200
                
            except ValueError as e:
                return {'error': str(e)}, 400
            except Exception as e:
                return {'error': 'Error interno del servidor'}, 500
    
    # === ENDPOINTS DE CHAT ===
    
    @chat_ns.route('/analyze')
    class BloodTestAnalysis(Resource):
        @chat_ns.doc('analyze_blood_test')
        @chat_ns.expect(models['blood_test_input'])
        @chat_ns.marshal_with(models['success_response'])
        @chat_ns.response(400, 'Datos de examen inválidos', models['error_response'])
        def post(self):
            """Analizar examen de sangre y crear conversación inicial con el chatbot"""
            try:
                data = request.get_json()
                
                # Validar datos requeridos
                if 'user_id' not in data:
                    return {'error': 'Campo requerido: user_id'}, 400
                
                # Validar que al menos algunos valores de examen estén presentes
                blood_test_fields = [
                    'glucose', 'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol',
                    'triglycerides', 'hemoglobin', 'hematocrit', 'white_blood_cells',
                    'red_blood_cells', 'platelets', 'creatinine', 'urea'
                ]
                
                present_fields = [field for field in blood_test_fields if field in data]
                if len(present_fields) < 3:
                    return {'error': 'Se requieren al menos 3 valores de examen de sangre'}, 400
                
                # Validar user_id (ya no necesita ser UUID)
                user_id = data['user_id']
                if not isinstance(user_id, str) or not user_id.strip():
                    return {'error': 'user_id debe ser una cadena válida'}, 400
                
                # Validar valores numéricos
                for field in present_fields:
                    if not isinstance(data[field], (int, float)) or data[field] < 0:
                        return {'error': f'{field} debe ser un número positivo'}, 400
                
                # Analizar examen
                result = chat_controller.analyze_blood_test_logic(user_id, data)
                
                return {
                    'success': True,
                    'message': 'Examen analizado exitosamente',
                    'data': result
                }, 200
                
            except ValueError as e:
                return {'error': str(e)}, 400
            except Exception as e:
                return {'error': 'Error interno del servidor'}, 500
    
    @chat_ns.route('/<string:conversation_id>/message')
    class ChatMessage(Resource):
        @chat_ns.doc('send_chat_message')
        @chat_ns.expect(models['chat_message_input'])
        @chat_ns.marshal_with(models['success_response'])
        @chat_ns.response(400, 'Mensaje inválido', models['error_response'])
        @chat_ns.response(404, 'Conversación no encontrada', models['error_response'])
        def post(self, conversation_id):
            """Enviar mensaje al chatbot en una conversación existente"""
            try:
                data = request.get_json()
                
                # Validar datos requeridos
                if 'message' not in data:
                    return {'error': 'Campo requerido: message'}, 400
                
                if not data['message'].strip():
                    return {'error': 'El mensaje no puede estar vacío'}, 400
                
                # Validar conversation_id
                if not isinstance(conversation_id, str) or not conversation_id.strip():
                    return {'error': 'conversation_id debe ser una cadena válida'}, 400
                
                # Procesar mensaje
                result = chat_controller.chat_message_logic(conversation_id, data['message'])
                
                return {
                    'success': True,
                    'data': result
                }, 200
                
            except ValueError as e:
                return {'error': str(e)}, 400
            except Exception as e:
                return {'error': 'Error interno del servidor'}, 500
    
    # === ENDPOINT DE SALUD ===
    
    @health_ns.route('')
    class HealthCheck(Resource):
        @health_ns.doc('health_check')
        @health_ns.marshal_with(models['health_response'])
        def get(self):
            """Verificar el estado de la API"""
            return {
                'status': 'healthy',
                'message': 'Medical Chatbot API is running'
            }, 200
    
    return api

class UserController:
    """Controlador para operaciones de usuarios"""
    
    def __init__(self, create_user_use_case: CreateUserUseCase, 
                 get_user_history_use_case: GetUserHistoryUseCase):
        self.create_user_use_case = create_user_use_case
        self.get_user_history_use_case = get_user_history_use_case
    
    def create_user_logic(self, data):
        """Lógica para crear usuario"""
        return self.create_user_use_case.execute(data)
    
    def get_user_history_logic(self, user_uuid):
        """Lógica para obtener historial de usuario"""
        return self.get_user_history_use_case.execute(user_uuid)

class ChatController:
    """Controlador para operaciones de chat"""
    
    def __init__(self, analyze_blood_test_use_case: AnalyzeBloodTestUseCase,
                 chat_with_user_use_case: ChatWithUserUseCase):
        self.analyze_blood_test_use_case = analyze_blood_test_use_case
        self.chat_with_user_use_case = chat_with_user_use_case
    
    def analyze_blood_test_logic(self, user_uuid, data):
        """Lógica para analizar examen de sangre"""
        return self.analyze_blood_test_use_case.execute(user_uuid, data)
    
    def chat_message_logic(self, conversation_uuid, message):
        """Lógica para procesar mensaje de chat"""
        return self.chat_with_user_use_case.execute(conversation_uuid, message)
