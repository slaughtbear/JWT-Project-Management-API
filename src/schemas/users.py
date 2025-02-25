from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    """Esquema base de usuario."""
    id: int
    username: str
    email: EmailStr
    created_at: str


class UserCreate(BaseModel):
    """Esquema para la creación de un usuario."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Esquema para actualizar datos del usuario."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)
