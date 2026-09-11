from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    photo_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class NewsCreate(BaseModel):
    title: str
    subtitle: Optional[str] = None
    text: str
    tags: List[str] = []

class NewsResponse(BaseModel):
    id: int
    title: str
    subtitle: Optional[str]
    text: str
    image_path: Optional[str]
    author: UserResponse
    tags: List[TagResponse]
    created_at: datetime
    comments_count: int = 0

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    text: str

class CommentResponse(BaseModel):
    id: int
    text: str
    author: UserResponse
    created_at: datetime

    class Config:
        from_attributes = True
