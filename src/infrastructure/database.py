from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Text, Integer
from datetime import datetime
import uuid

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    blood_tests = db.relationship("BloodTestModel", back_populates="user", cascade="all, delete-orphan")
    conversations = db.relationship("ChatConversationModel", back_populates="user", cascade="all, delete-orphan")

class BloodTestModel(db.Model):
    __tablename__ = 'blood_tests'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    glucose = Column(Float, nullable=True)
    cholesterol = Column(Float, nullable=True)
    hdl_cholesterol = Column(Float, nullable=True)
    ldl_cholesterol = Column(Float, nullable=True)
    triglycerides = Column(Float, nullable=True)
    hemoglobin = Column(Float, nullable=True)
    hematocrit = Column(Float, nullable=True)
    white_blood_cells = Column(Float, nullable=True)
    red_blood_cells = Column(Float, nullable=True)
    platelets = Column(Float, nullable=True)
    creatinine = Column(Float, nullable=True)
    urea = Column(Float, nullable=True)
    test_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = db.relationship("UserModel", back_populates="blood_tests")
    conversations = db.relationship("ChatConversationModel", back_populates="blood_test")

class ChatConversationModel(db.Model):
    __tablename__ = 'chat_conversations'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    blood_test_id = Column(String(36), ForeignKey('blood_tests.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = db.relationship("UserModel", back_populates="conversations")
    blood_test = db.relationship("BloodTestModel", back_populates="conversations")
    messages = db.relationship("ChatMessageModel", back_populates="conversation", cascade="all, delete-orphan")

class ChatMessageModel(db.Model):
    __tablename__ = 'chat_messages'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('chat_conversations.id'), nullable=False)
    content = Column(Text, nullable=False)
    sender = Column(String(20), nullable=False)  # 'user' o 'assistant'
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    conversation = db.relationship("ChatConversationModel", back_populates="messages")
