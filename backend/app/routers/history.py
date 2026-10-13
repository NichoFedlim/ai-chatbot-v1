"""
History router for managing chat history.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import logging

from ..database import get_db
from ..models import ChatMessage
from ..schemas import (
    HistoryResponse, MessageSchema, DeleteMessageResponse, 
    ClearHistoryResponse, ErrorResponse
)
from ..config import settings

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["history"])

@router.get("/history", response_model=HistoryResponse)
async def get_history(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get chat history with pagination.
    """
    try:
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Get total count of non-deleted messages
        total_count = db.query(func.count(ChatMessage.id))\
            .filter(ChatMessage.is_deleted == False)\
            .scalar()
        
        # Get paginated messages
        messages = db.query(ChatMessage)\
            .filter(ChatMessage.is_deleted == False)\
            .order_by(ChatMessage.timestamp.desc())\
            .offset(offset)\
            .limit(page_size)\
            .all()
        
        # Reverse to show oldest first in response
        messages.reverse()
        
        return HistoryResponse(
            messages=[MessageSchema.from_orm(msg) for msg in messages],
            total_count=total_count,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat history")

@router.delete("/history/{message_id}", response_model=DeleteMessageResponse)
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a specific message.
    """
    try:
        message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
        
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        if message.is_deleted:
            raise HTTPException(status_code=400, detail="Message already deleted")
        
        # Soft delete
        message.is_deleted = True
        db.commit()
        
        return DeleteMessageResponse(
            success=True,
            message="Message deleted successfully",
            deleted_id=message_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting message: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete message")

@router.post("/clear", response_model=ClearHistoryResponse)
async def clear_history(db: Session = Depends(get_db)):
    """
    Clear all chat history (soft delete all messages).
    """
    try:
        # Count non-deleted messages
        deleted_count = db.query(ChatMessage)\
            .filter(ChatMessage.is_deleted == False)\
            .update({ChatMessage.is_deleted: True})
        
        db.commit()
        
        return ClearHistoryResponse(
            success=True,
            message="Chat history cleared successfully",
            deleted_count=deleted_count
        )
        
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to clear chat history")
    