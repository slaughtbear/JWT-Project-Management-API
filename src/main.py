from fastapi import FastAPI
from src.routes.tasks import tasks_router
from src.routes.projects import projects_router
from src.routes.authentication import auth_router
from src.routes.users import users_router


app = FastAPI()


app.include_router(
    users_router,
    prefix = "/user",
    tags = ["User"]
)


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
    auth_router,
    tags = ["Authentication"]
)