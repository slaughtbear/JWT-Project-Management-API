from fastapi import APIRouter, HTTPException, status
from typing import List
from src.schemas.project import Project
from src.utils.functions import internal_server_error_exception
from src.database.querys.projects import get_all_projects_bd


projects_router = APIRouter()


@projects_router.get("/", response_model = List[Project])
async def get_projects() -> List[Project]:
    try:
        projects = get_all_projects_bd()
    except Exception as e:
        internal_server_error_exception(e)

    if not projects:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontró ninguna tarea..."
        )
    
    return projects