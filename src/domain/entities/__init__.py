from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import uuid

@dataclass
class User:
    """Entidad Usuario del dominio"""
    id: str
    name: str
    age: int
    gender: str
    created_at: datetime
    
    @classmethod
    def create(cls, name: str, age: int, gender: str) -> 'User':
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            age=age,
            gender=gender,
            created_at=datetime.now()
        )

@dataclass
class BloodTest:
    """Entidad Examen de Sangre"""
    id: str
    user_id: str
    glucose: float
    cholesterol: float
    hdl_cholesterol: float
    ldl_cholesterol: float
    triglycerides: float
    hemoglobin: float
    hematocrit: float
    white_blood_cells: float
    red_blood_cells: float
    platelets: float
    creatinine: float
    urea: float
    test_date: datetime
    created_at: datetime
    
    @classmethod
    def create(cls, user_id: str, test_data: dict, test_date: datetime) -> 'BloodTest':
        return cls(
            id=str(uuid.uuid4()),
            user_id=user_id,
            glucose=test_data.get('glucose', 0.0),
            cholesterol=test_data.get('cholesterol', 0.0),
            hdl_cholesterol=test_data.get('hdl_cholesterol', 0.0),
            ldl_cholesterol=test_data.get('ldl_cholesterol', 0.0),
            triglycerides=test_data.get('triglycerides', 0.0),
            hemoglobin=test_data.get('hemoglobin', 0.0),
            hematocrit=test_data.get('hematocrit', 0.0),
            white_blood_cells=test_data.get('white_blood_cells', 0.0),
            red_blood_cells=test_data.get('red_blood_cells', 0.0),
            platelets=test_data.get('platelets', 0.0),
            creatinine=test_data.get('creatinine', 0.0),
            urea=test_data.get('urea', 0.0),
            test_date=test_date,
            created_at=datetime.now()
        )

@dataclass
class ChatConversation:
    """Entidad Conversación de Chat"""
    id: str
    user_id: str
    blood_test_id: Optional[str]
    messages: List['ChatMessage']
    created_at: datetime
    
    @classmethod
    def create(cls, user_id: str, blood_test_id: Optional[str] = None) -> 'ChatConversation':
        return cls(
            id=str(uuid.uuid4()),
            user_id=user_id,
            blood_test_id=blood_test_id,
            messages=[],
            created_at=datetime.now()
        )
    
    def add_message(self, message: 'ChatMessage'):
        self.messages.append(message)

@dataclass
class ChatMessage:
    """Entidad Mensaje de Chat"""
    id: str
    conversation_id: str
    content: str
    sender: str  # 'user' o 'assistant'
    timestamp: datetime
    
    @classmethod
    def create(cls, conversation_id: str, content: str, sender: str) -> 'ChatMessage':
        return cls(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            content=content,
            sender=sender,
            timestamp=datetime.now()
        )
