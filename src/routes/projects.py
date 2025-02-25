from fastapi import APIRouter, Path, HTTPException, status
from typing import List, Dict
from src.schemas.project import Project, ProjectCreate, ProjectUpdate
from src.database.querys.projects import (
    get_all_projects_bd, create_project_bd, 
    update_project_bd, delete_project_bd
)
from src.utils.functions import internal_server_error_exception, search_project

projects_router = APIRouter()


@projects_router.get("/", response_model=List[Project])
async def get_projects() -> List[Project]:
    try:
        projects = get_all_projects_bd()
    except Exception as e:
        internal_server_error_exception(e)

    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró ningún proyecto..."
        )
    
    return projects


@projects_router.get("/{id}", response_model=Project)
async def get_project_by_id(id: int = Path(gt=0)) -> Project:
    ''' Endpoint para obtener un proyecto por ID.'''
    return search_project(id)


@projects_router.post("/", response_model=Project)
async def add_project(project_data: ProjectCreate) -> Project:
    ''' Endpoint para agregar proyectos a la base de datos. '''
    try:
        return create_project_bd(project_data)
    except Exception as e:
        internal_server_error_exception(e)


@projects_router.put("/{id}", response_model=Project)
async def update_project(project_data: ProjectUpdate, id: int = Path(gt=0)) -> Project:
    ''' Endpoint para actualizar proyectos de la base de datos. '''
    if search_project(id):
        try:
            return update_project_bd(project_data, id)
        except Exception as e:
            internal_server_error_exception(e)


@projects_router.delete("/{id}")
async def delete_project(id: int = Path(gt=0)) -> Dict:
    ''' Endpoint para eliminar un proyecto de la base de datos. '''
    if search_project(id):
        try:
            delete_project_bd(id)
        except Exception as e:
            internal_server_error_exception(e)
        return {"detail": "Proyecto eliminado correctamente."}
