from fastapi import FastAPI
from src.routes.tasks import tasks_router

app = FastAPI()

@app.get("/")
async def main():
    return {"message": "welcome to my to-do list api"}

app.include_router(
    tasks_router,
    prefix = "/tasks",
    tags = ["Tasks"]
)