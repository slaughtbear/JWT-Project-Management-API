from fastapi import APIRouter, Path, HTTPException, status
from fastapi.responses import JSONResponse
from src.schemas.task import Task, TaskCreate
from src.database.querys.tasks import get_all_tasks, get_one_task, create_task
from src.utils.functions import internal_server_error_exception, validate_task



tasks_router = APIRouter()


@tasks_router.get("/")
async def get_tasks():
    try:
        tasks = get_all_tasks()
    except Exception as e: 
        internal_server_error_exception(e)

    if not tasks:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontró ninguna tarea..."
        )
    return JSONResponse(content = tasks)


@tasks_router.get("/{id}", response_model = Task)
async def get_task_by_id(id: int = Path(gt = 0)) -> Task:
    try:
        task = get_one_task(id)
    except Exception as e: 
        internal_server_error_exception(e)

    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontró ninguna tarea."
        )
    return JSONResponse(content = task)


@tasks_router.post("/")
async def add_task(task_data: TaskCreate) -> Task:
    validate_task(task_data)
    try:
        new_task = create_task(task_data)
        return JSONResponse(content = new_task)
    except Exception as e:
        internal_server_error_exception(e)
            
        





