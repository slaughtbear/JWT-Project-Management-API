from pydantic import BaseModel, Field
from typing import Optional


class Project(BaseModel):
    """Esquema base para un proyecto."""
    id: int
    created_at: str
    name: str
    description: Optional[str] = None


class ProjectCreate(BaseModel):
    """Esquema para la creación de un proyecto."""
    name: str = Field(max_length=100, min_length=3)
    description: Optional[str] = Field(None, max_length=255)


class ProjectUpdate(BaseModel):
    """Esquema para actualizar datos del proyecto."""
    name: Optional[str] = Field(None, max_length=100, min_length=3)
    description: Optional[str] = Field(None, max_length=255)
