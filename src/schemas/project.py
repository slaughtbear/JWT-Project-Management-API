from pydantic import BaseModel

class Project(BaseModel):
    id: int
    name: str

projects_list = [
    Project(1, 'app fullstack con react y django')
]