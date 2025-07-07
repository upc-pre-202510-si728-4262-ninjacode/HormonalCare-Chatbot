from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Importar componentes
from src.infrastructure.database import db
from src.infrastructure.sqlalchemy_repositories import (
    SQLAlchemyUserRepository,
    SQLAlchemyBloodTestRepository,
    SQLAlchemyChatConversationRepository,
    SQLAlchemyChatMessageRepository
)
from src.infrastructure.gemini_service import GeminiService
from src.application.use_cases import (
    CreateUserUseCase,
    AnalyzeBloodTestUseCase,
    ChatWithUserUseCase,
    GetUserHistoryUseCase
)
from src.presentation.controllers import UserController, ChatController, create_api

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///medical_chatbot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app)
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    # Inicializar repositorios
    user_repository = SQLAlchemyUserRepository()
    blood_test_repository = SQLAlchemyBloodTestRepository()
    conversation_repository = SQLAlchemyChatConversationRepository()
    message_repository = SQLAlchemyChatMessageRepository()
    
    # Inicializar servicios
    gemini_service = GeminiService()
    
    # Inicializar casos de uso
    create_user_use_case = CreateUserUseCase(user_repository)
    analyze_blood_test_use_case = AnalyzeBloodTestUseCase(
        user_repository,
        blood_test_repository,
        conversation_repository,
        message_repository,
        gemini_service
    )
    chat_with_user_use_case = ChatWithUserUseCase(
        user_repository,
        blood_test_repository,
        conversation_repository,
        message_repository,
        gemini_service
    )
    get_user_history_use_case = GetUserHistoryUseCase(
        user_repository,
        blood_test_repository,
        conversation_repository
    )
    
    # Factory functions para controladores
    def user_controller_factory():
        return UserController(create_user_use_case, get_user_history_use_case)
    
    def chat_controller_factory():
        return ChatController(analyze_blood_test_use_case, chat_with_user_use_case)
    
    # Crear API con Swagger
    api = create_api(app, user_controller_factory, chat_controller_factory)
    
    print("🏥 Medical Chatbot API iniciada")
    print("📖 Documentación Swagger disponible en: http://localhost:5000/docs/")
    
    return app

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
