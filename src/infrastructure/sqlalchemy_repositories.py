from typing import Optional, List
from datetime import datetime
from .repositories import UserRepository, BloodTestRepository, ChatConversationRepository, ChatMessageRepository
from .database import db, UserModel, BloodTestModel, ChatConversationModel, ChatMessageModel
from ..domain.entities import User, BloodTest, ChatConversation, ChatMessage

class SQLAlchemyUserRepository(UserRepository):
    """Implementación SQLAlchemy del repositorio de usuarios"""
    
    def save(self, user: User) -> User:
        user_model = UserModel(
            id=user.id,
            name=user.name,
            age=user.age,
            gender=user.gender,
            created_at=user.created_at
        )
        db.session.add(user_model)
        db.session.commit()
        return user
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        user_model = UserModel.query.filter_by(id=user_id).first()
        if user_model:
            return User(
                id=user_model.id,
                name=user_model.name,
                age=user_model.age,
                gender=user_model.gender,
                created_at=user_model.created_at
            )
        return None
    
    def get_all(self) -> List[User]:
        user_models = UserModel.query.all()
        return [
            User(
                id=user_model.id,
                name=user_model.name,
                age=user_model.age,
                gender=user_model.gender,
                created_at=user_model.created_at
            ) for user_model in user_models
        ]

class SQLAlchemyBloodTestRepository(BloodTestRepository):
    """Implementación SQLAlchemy del repositorio de exámenes de sangre"""
    
    def save(self, blood_test: BloodTest) -> BloodTest:
        blood_test_model = BloodTestModel(
            id=blood_test.id,
            user_id=blood_test.user_id,
            glucose=blood_test.glucose,
            cholesterol=blood_test.cholesterol,
            hdl_cholesterol=blood_test.hdl_cholesterol,
            ldl_cholesterol=blood_test.ldl_cholesterol,
            triglycerides=blood_test.triglycerides,
            hemoglobin=blood_test.hemoglobin,
            hematocrit=blood_test.hematocrit,
            white_blood_cells=blood_test.white_blood_cells,
            red_blood_cells=blood_test.red_blood_cells,
            platelets=blood_test.platelets,
            creatinine=blood_test.creatinine,
            urea=blood_test.urea,
            test_date=blood_test.test_date,
            created_at=blood_test.created_at
        )
        db.session.add(blood_test_model)
        db.session.commit()
        return blood_test
    
    def get_by_id(self, test_id: str) -> Optional[BloodTest]:
        test_model = BloodTestModel.query.filter_by(id=test_id).first()
        if test_model:
            return self._model_to_entity(test_model)
        return None
    
    def get_by_user_id(self, user_id: str) -> List[BloodTest]:
        test_models = BloodTestModel.query.filter_by(user_id=user_id).order_by(BloodTestModel.test_date.desc()).all()
        return [self._model_to_entity(model) for model in test_models]
    
    def get_latest_by_user_id(self, user_id: str) -> Optional[BloodTest]:
        test_model = BloodTestModel.query.filter_by(user_id=user_id).order_by(BloodTestModel.test_date.desc()).first()
        if test_model:
            return self._model_to_entity(test_model)
        return None
    
    def _model_to_entity(self, model: BloodTestModel) -> BloodTest:
        return BloodTest(
            id=model.id,
            user_id=model.user_id,
            glucose=model.glucose,
            cholesterol=model.cholesterol,
            hdl_cholesterol=model.hdl_cholesterol,
            ldl_cholesterol=model.ldl_cholesterol,
            triglycerides=model.triglycerides,
            hemoglobin=model.hemoglobin,
            hematocrit=model.hematocrit,
            white_blood_cells=model.white_blood_cells,
            red_blood_cells=model.red_blood_cells,
            platelets=model.platelets,
            creatinine=model.creatinine,
            urea=model.urea,
            test_date=model.test_date,
            created_at=model.created_at
        )

class SQLAlchemyChatConversationRepository(ChatConversationRepository):
    """Implementación SQLAlchemy del repositorio de conversaciones"""
    
    def save(self, conversation: ChatConversation) -> ChatConversation:
        conversation_model = ChatConversationModel(
            id=conversation.id,
            user_id=conversation.user_id,
            blood_test_id=conversation.blood_test_id,
            created_at=conversation.created_at
        )
        db.session.add(conversation_model)
        db.session.commit()
        return conversation
    
    def get_by_id(self, conversation_id: str) -> Optional[ChatConversation]:
        conversation_model = ChatConversationModel.query.filter_by(id=conversation_id).first()
        if conversation_model:
            # Cargar mensajes
            message_models = ChatMessageModel.query.filter_by(conversation_id=conversation_id).order_by(ChatMessageModel.timestamp).all()
            messages = [
                ChatMessage(
                    id=msg.id,
                    conversation_id=msg.conversation_id,
                    content=msg.content,
                    sender=msg.sender,
                    timestamp=msg.timestamp
                ) for msg in message_models
            ]
            
            return ChatConversation(
                id=conversation_model.id,
                user_id=conversation_model.user_id,
                blood_test_id=conversation_model.blood_test_id,
                messages=messages,
                created_at=conversation_model.created_at
            )
        return None
    
    def get_by_user_id(self, user_id: str) -> List[ChatConversation]:
        conversation_models = ChatConversationModel.query.filter_by(user_id=user_id).order_by(ChatConversationModel.created_at.desc()).all()
        conversations = []
        
        for conv_model in conversation_models:
            # Cargar mensajes para cada conversación
            message_models = ChatMessageModel.query.filter_by(conversation_id=conv_model.id).order_by(ChatMessageModel.timestamp).all()
            messages = [
                ChatMessage(
                    id=msg.id,
                    conversation_id=msg.conversation_id,
                    content=msg.content,
                    sender=msg.sender,
                    timestamp=msg.timestamp
                ) for msg in message_models
            ]
            
            conversations.append(ChatConversation(
                id=conv_model.id,
                user_id=conv_model.user_id,
                blood_test_id=conv_model.blood_test_id,
                messages=messages,
                created_at=conv_model.created_at
            ))
        
        return conversations

class SQLAlchemyChatMessageRepository(ChatMessageRepository):
    """Implementación SQLAlchemy del repositorio de mensajes"""
    
    def save(self, message: ChatMessage) -> ChatMessage:
        message_model = ChatMessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            content=message.content,
            sender=message.sender,
            timestamp=message.timestamp
        )
        db.session.add(message_model)
        db.session.commit()
        return message
    
    def get_by_conversation_id(self, conversation_id: str) -> List[ChatMessage]:
        message_models = ChatMessageModel.query.filter_by(conversation_id=conversation_id).order_by(ChatMessageModel.timestamp).all()
        return [
            ChatMessage(
                id=msg.id,
                conversation_id=msg.conversation_id,
                content=msg.content,
                sender=msg.sender,
                timestamp=msg.timestamp
            ) for msg in message_models
        ]
