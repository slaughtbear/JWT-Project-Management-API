from pydantic import BaseModel, Field
from typing import Optional


class Task(BaseModel):
    id: int
    created_at: str
    title: str
    description: str
    project_id: int


class TaskCreate(BaseModel):
    title: str = Field(max_length = 64, min_length = 10)
    description: str = Field(max_length = 364, min_length = 10)
    project_id: int = Field(gt = 0)


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None