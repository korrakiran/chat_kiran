from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, create_engine
import uuid

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    picture: Optional[str] = None
    preferences: Optional[str] = None  # JSON string
    context: Optional[str] = None  # Persistent memory context
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    chats: List["Chat"] = Relationship(back_populates="user")

class Chat(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str = Field(default="New Chat")
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: User = Relationship(back_populates="chats")
    messages: List["Message"] = Relationship(back_populates="chat")

class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    chat_id: str = Field(foreign_key="chat.id")
    role: str  # user / assistant / system
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    chat: Chat = Relationship(back_populates="messages")
