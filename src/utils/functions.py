from fastapi import HTTPException, status
from src.database.querys.tasks import get_one_task_by_title
from src.database.querys.projects import get_one_project


def internal_server_error_exception(e):
    print(f"Error: {e}")
    raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor."
        )


def validate_task(task_data):
    try:
        stored_task_title = get_one_task_by_title(task_data.title)
        stored_project = get_one_project(task_data.project_id)
    except Exception as e:
        internal_server_error_exception(e)

    if stored_task_title:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Ya existe una tarea con ese título en la base de datos."
        )
    
    if not stored_project:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontró el id del proyecto al que pertenece la tarea."
        )