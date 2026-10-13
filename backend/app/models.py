"""
Database models for chat messages.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base

class ChatMessage(Base):
    """Model representing a chat message."""
    
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # Optional metadata
    model = Column(String(100), nullable=True)  # AI model used
    tokens_used = Column(Integer, nullable=True)  # Token count
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "is_deleted": self.is_deleted,
            "model": self.model,
            "tokens_used": self.tokens_used
        }
    
    def __repr__(self) -> str:
        return f"<ChatMessage {self.id}: {self.role} - {self.content[:50]}...>"
    