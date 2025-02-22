from fastapi import FastAPI
from src.routes.tasks import tasks_router
from src.routes.projects import projects_router
from src.routes.jwt_auth import jwt_auth


app = FastAPI()


@app.get("/")
async def main():
    return {"message": "welcome to my to-do list api"}


app.include_router(
    tasks_router,
    prefix = "/tasks",
    tags = ["Tasks"]
)


app.include_router(
    projects_router,
    prefix = "/projects",
    tags = ["Projects"]
)


app.include_router(
    jwt_auth,
    prefix = "/auth",
    tags = ["Authentication"]
)