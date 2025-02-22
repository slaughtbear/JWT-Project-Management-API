from pydantic import BaseModel

class Project(BaseModel):
    id: int
    created_at: str
    name: str