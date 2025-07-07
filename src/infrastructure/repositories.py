from abc import ABC, abstractmethod
from typing import Optional, List
from ..domain.entities import User, BloodTest, ChatConversation, ChatMessage

class UserRepository(ABC):
    """Repositorio abstracto para usuarios"""
    
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[User]:
        pass

class BloodTestRepository(ABC):
    """Repositorio abstracto para exámenes de sangre"""
    
    @abstractmethod
    def save(self, blood_test: BloodTest) -> BloodTest:
        pass
    
    @abstractmethod
    def get_by_id(self, test_id: str) -> Optional[BloodTest]:
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> List[BloodTest]:
        pass
    
    @abstractmethod
    def get_latest_by_user_id(self, user_id: str) -> Optional[BloodTest]:
        pass

class ChatConversationRepository(ABC):
    """Repositorio abstracto para conversaciones de chat"""
    
    @abstractmethod
    def save(self, conversation: ChatConversation) -> ChatConversation:
        pass
    
    @abstractmethod
    def get_by_id(self, conversation_id: str) -> Optional[ChatConversation]:
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> List[ChatConversation]:
        pass

class ChatMessageRepository(ABC):
    """Repositorio abstracto para mensajes de chat"""
    
    @abstractmethod
    def save(self, message: ChatMessage) -> ChatMessage:
        pass
    
    @abstractmethod
    def get_by_conversation_id(self, conversation_id: str) -> List[ChatMessage]:
        pass
