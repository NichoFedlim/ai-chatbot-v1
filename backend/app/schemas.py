"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=4000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID")
    
    @validator('message')
    def validate_message(cls, v: str) -> str:
        """Validate and clean message."""
        # Strip whitespace
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        return v

class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    message: str
    conversation_id: str
    timestamp: datetime
    model: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[int] = None

class MessageSchema(BaseModel):
    """Schema for individual message."""
    id: int
    role: str
    content: str
    timestamp: datetime
    is_deleted: bool = False
    model: Optional[str] = None
    
    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    """Response schema for history endpoint."""
    messages: List[MessageSchema]
    total_count: int
    page: int
    page_size: int

class DeleteMessageResponse(BaseModel):
    """Response schema for delete endpoint."""
    success: bool
    message: str
    deleted_id: int

class ClearHistoryResponse(BaseModel):
    """Response schema for clear history endpoint."""
    success: bool
    message: str
    deleted_count: int

class ErrorResponse(BaseModel):
    """Standard error response schema."""
    error: str
    detail: Optional[str] = None
    status_code: int
    