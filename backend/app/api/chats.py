from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..db.session import get_session
from ..db.models import Chat, User
# Auth dependency to be implemented in core/security.py
# from ..core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Chat])
async def list_chats(db: Session = Depends(get_session)):
    # In a real app, filter by current_user.id
    chats = db.exec(select(Chat)).all()
    return chats

@router.post("/create", response_model=Chat)
async def create_chat(chat_data: Chat, db: Session = Depends(get_session)):
    # Assign current_user.id if implementing auth
    db.add(chat_data)
    db.commit()
    db.refresh(chat_data)
    return chat_data

@router.get("/{id}", response_model=Chat)
async def get_chat(id: str, db: Session = Depends(get_session)):
    chat = db.get(Chat, id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
