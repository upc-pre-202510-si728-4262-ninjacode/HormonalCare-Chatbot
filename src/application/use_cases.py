from typing import Dict, Any, Optional
from datetime import datetime
from ..domain.entities import User, BloodTest, ChatConversation, ChatMessage
from ..domain.services import BloodTestAnalysisService
from ..infrastructure.repositories import UserRepository, BloodTestRepository, ChatConversationRepository, ChatMessageRepository
from ..infrastructure.gemini_service import GeminiService

class CreateUserUseCase:
    """Caso de uso para crear un usuario"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        # Crear nuevo usuario (sin verificar email duplicado)
        user = User.create(
            name=user_data['name'],
            age=user_data['age'],
            gender=user_data['gender']
        )
        
        # Guardar usuario
        saved_user = self.user_repository.save(user)
        
        return {
            'id': str(saved_user.id),
            'name': saved_user.name,
            'age': saved_user.age,
            'gender': saved_user.gender,
            'created_at': saved_user.created_at.isoformat()
        }

class AnalyzeBloodTestUseCase:
    """Caso de uso para analizar un examen de sangre"""
    
    def __init__(self, 
                 user_repository: UserRepository,
                 blood_test_repository: BloodTestRepository,
                 conversation_repository: ChatConversationRepository,
                 message_repository: ChatMessageRepository,
                 gemini_service: GeminiService):
        self.user_repository = user_repository
        self.blood_test_repository = blood_test_repository
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.gemini_service = gemini_service
        self.analysis_service = BloodTestAnalysisService()
    
    def execute(self, user_id: str, blood_test_data: Dict[str, Any]) -> Dict[str, Any]:
        # Obtener usuario
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Crear examen de sangre
        test_date = datetime.fromisoformat(blood_test_data.get('test_date', datetime.now().isoformat()))
        blood_test = BloodTest.create(
            user_id=user_id,
            test_data=blood_test_data,
            test_date=test_date
        )
        
        # Guardar examen
        saved_test = self.blood_test_repository.save(blood_test)
        
        # Realizar análisis
        analysis = self.analysis_service.analyze_blood_test(saved_test, user)
        
        # Generar explicación con IA
        user_data = {
            'name': user.name,
            'age': user.age,
            'gender': user.gender
        }
        
        ai_explanation = self.gemini_service.analyze_blood_test_with_ai(
            blood_test_data, user_data, analysis.to_dict()
        )
        
        # Crear conversación inicial
        conversation = ChatConversation.create(user_id=user_id, blood_test_id=saved_test.id)
        saved_conversation = self.conversation_repository.save(conversation)
        
        # Crear mensaje inicial del asistente
        initial_message = ChatMessage.create(
            conversation_id=saved_conversation.id,
            content=ai_explanation,
            sender='assistant'
        )
        self.message_repository.save(initial_message)
        
        return {
            'blood_test_id': str(saved_test.id),
            'conversation_id': str(saved_conversation.id),
            'analysis': analysis.to_dict(),
            'ai_explanation': ai_explanation
        }

class ChatWithUserUseCase:
    """Caso de uso para chatear con el usuario"""
    
    def __init__(self,
                 user_repository: UserRepository,
                 blood_test_repository: BloodTestRepository,
                 conversation_repository: ChatConversationRepository,
                 message_repository: ChatMessageRepository,
                 gemini_service: GeminiService):
        self.user_repository = user_repository
        self.blood_test_repository = blood_test_repository
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.gemini_service = gemini_service
        self.analysis_service = BloodTestAnalysisService()
    
    def execute(self, conversation_id: str, user_message: str) -> Dict[str, Any]:
        # Obtener conversación
        conversation = self.conversation_repository.get_by_id(conversation_id)
        if not conversation:
            raise ValueError("Conversación no encontrada")
        
        # Obtener usuario
        user = self.user_repository.get_by_id(conversation.user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Obtener último examen de sangre
        blood_test = None
        blood_test_data = {}
        analysis_data = {}
        
        if conversation.blood_test_id:
            blood_test = self.blood_test_repository.get_by_id(conversation.blood_test_id)
        else:
            blood_test = self.blood_test_repository.get_latest_by_user_id(conversation.user_id)
        
        if blood_test:
            blood_test_data = {
                'glucose': blood_test.glucose,
                'cholesterol': blood_test.cholesterol,
                'hdl_cholesterol': blood_test.hdl_cholesterol,
                'ldl_cholesterol': blood_test.ldl_cholesterol,
                'triglycerides': blood_test.triglycerides,
                'hemoglobin': blood_test.hemoglobin,
                'hematocrit': blood_test.hematocrit,
                'white_blood_cells': blood_test.white_blood_cells,
                'red_blood_cells': blood_test.red_blood_cells,
                'platelets': blood_test.platelets,
                'creatinine': blood_test.creatinine,
                'urea': blood_test.urea
            }
            
            # Realizar análisis del examen
            analysis = self.analysis_service.analyze_blood_test(blood_test, user)
            analysis_data = analysis.to_dict()
        
        # Guardar mensaje del usuario
        user_msg = ChatMessage.create(
            conversation_id=conversation_id,
            content=user_message,
            sender='user'
        )
        self.message_repository.save(user_msg)
        
        # Generar respuesta con IA
        user_data = {
            'name': user.name,
            'age': user.age,
            'gender': user.gender
        }
        
        ai_response = self.gemini_service.chat_with_user(
            user_message, blood_test_data, user_data, analysis_data
        )
        
        # Guardar respuesta del asistente
        assistant_msg = ChatMessage.create(
            conversation_id=conversation_id,
            content=ai_response,
            sender='assistant'
        )
        self.message_repository.save(assistant_msg)
        
        return {
            'user_message': user_message,
            'assistant_response': ai_response,
            'timestamp': assistant_msg.timestamp.isoformat()
        }

class GetUserHistoryUseCase:
    """Caso de uso para obtener el historial de un usuario"""
    
    def __init__(self,
                 user_repository: UserRepository,
                 blood_test_repository: BloodTestRepository,
                 conversation_repository: ChatConversationRepository):
        self.user_repository = user_repository
        self.blood_test_repository = blood_test_repository
        self.conversation_repository = conversation_repository
    
    def execute(self, user_id: str) -> Dict[str, Any]:
        # Verificar que el usuario existe
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        # Obtener exámenes de sangre
        blood_tests = self.blood_test_repository.get_by_user_id(user_id)
        
        # Obtener conversaciones
        conversations = self.conversation_repository.get_by_user_id(user_id)
        
        return {
            'user': {
                'id': str(user.id),
                'name': user.name,
                'age': user.age,
                'gender': user.gender
            },
            'blood_tests': [
                {
                    'id': str(test.id),
                    'glucose': test.glucose,
                    'cholesterol': test.cholesterol,
                    'test_date': test.test_date.isoformat(),
                    'created_at': test.created_at.isoformat()
                } for test in blood_tests
            ],
            'conversations': [
                {
                    'id': str(conv.id),
                    'blood_test_id': str(conv.blood_test_id) if conv.blood_test_id else None,
                    'created_at': conv.created_at.isoformat(),
                    'message_count': len(conv.messages)
                } for conv in conversations
            ]
        }
