"""
Chat router for handling chat requests.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Dict
import uuid
import logging
from datetime import datetime

from ..database import get_db
from ..models import ChatMessage
from ..schemas import ChatRequest, ChatResponse, ErrorResponse
from ..services.ai_service import ai_service
from ..middleware.rate_limit import rate_limit

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/chat", response_model=ChatResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
@rate_limit()
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Send a message and get AI response.
    """
    try:
        # Save user message to database
        user_message = ChatMessage(
            role="user",
            content=request.message,
            timestamp=datetime.utcnow()
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Get chat history for context
        history = await get_recent_history(db, limit=10)
        
        # Get AI response
        ai_response = await ai_service.get_response(request.message, history)
        
        # Save AI response to database
        assistant_message = ChatMessage(
            role="assistant",
            content=ai_response["message"],
            timestamp=datetime.utcnow(),
            model=ai_response.get("model"),
            tokens_used=ai_response.get("tokens_used")
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        # Return response
        return ChatResponse(
            message=ai_response["message"],
            conversation_id=str(uuid.uuid4()),
            timestamp=assistant_message.timestamp,
            model=ai_response.get("model", "unknown"),
            tokens_used=ai_response.get("tokens_used"),
            latency_ms=ai_response.get("latency_ms")
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat request: {str(e)}"
        )

async def get_recent_history(db: Session, limit: int = 10) -> List[Dict[str, str]]:
    """Get recent chat history for context."""
    messages = db.query(ChatMessage)\
        .filter(ChatMessage.is_deleted == False)\
        .order_by(ChatMessage.timestamp.desc())\
        .limit(limit)\
        .all()
    
    # Reverse to chronological order
    messages.reverse()
    
    return [{"role": msg.role, "content": msg.content} for msg in messages]
