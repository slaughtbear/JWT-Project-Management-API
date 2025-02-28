# FastAPI
from fastapi import APIRouter, Path, HTTPException, status

# Tipos de datos
from typing import List, Dict

# Esquemas Pydantic
from src.schemas.project import Project, ProjectCreate, ProjectUpdate

# Base de datos
from src.database.querys.projects import (
    get_all_projects_bd,
    create_project_bd,
    update_project_bd,
    delete_project_bd
)

# Funciones auxiliares
from src.utils.functions import internal_server_error_exception, search_project

# Dependencias
from src.dependencies.dependencies import GetCurrentUser, IdValidator


projects_router = APIRouter()


@projects_router.get("/", response_model=List[Project])
async def get_projects(current_user: GetCurrentUser) -> List[Project]:
    """ Endpoint para que un usuario obtenga todos sus proyectos almacenados en la base de datos.

    Args:
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.

    Returns:
        projects (List[Project]): Lista de los proyectos que le pertenecen al usuario que realizó la petición.
    """
    try:
        projects = get_all_projects_bd(current_user["id"])
    except Exception as e:
        internal_server_error_exception(e)

    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró ningún proyecto..."
        )
    
    return projects


@projects_router.get("/{id}", response_model=Project)
async def get_project_by_id(current_user: GetCurrentUser, id: IdValidator) -> Project:
    """Endpoint para que un usuario obtenga un proyecto en específico mediante un ID.
    
    Args:
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.
        id (IdValidator): Es el ID del proyecto a buscar, este incluye una dependencia para validar que el ID sea mayor a 0.

    Returns:
        Project: Proyecto buscado por el usuario.
    """
    return search_project(id, current_user["id"])


@projects_router.post("/", response_model=Project)
async def add_project(project_data: ProjectCreate, current_user: GetCurrentUser) -> Project:
    """Endpoint para que un usuario pueda crear un proyecto nuevo.

    Args:
        project_data (ProjectCreate): Datos solicitados para crear el proyecto nuevo.
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.


    Returns:
        Project: Proyecto creado por el usuario.
    
    """
    try:
        return create_project_bd(project_data, current_user)
    except Exception as e:
        internal_server_error_exception(e)


@projects_router.put("/{id}", response_model=Project)
async def update_project(project_data: ProjectUpdate, current_user: GetCurrentUser, id: IdValidator) -> Project:
    """Endpoint para que un usuario pueda actualizar un proyecto.

    Args:
        project_data (ProjectUpdate): Datos "actualizados" de un proyecto.
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.
        id: ID del proyecto a actualizar.

    Returns:
        Project: Proyecto con los datos actualizados.
    """
    if search_project(id, current_user["id"]):
        try:
            return update_project_bd(project_data, id)
        except Exception as e:
            internal_server_error_exception(e)


@projects_router.delete("/{id}")
async def delete_project(current_user: GetCurrentUser, id: IdValidator) -> Dict:
    """Endpoint para eliminar un proyecto.
    
    Args:
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.
        id: ID del proyecto a eliminar.

    Returns:
        Dict: Diccionario con un mensaje para validar que se eliminó el proyecto.
    """
    if search_project(id, current_user["id"]):
        try:
            delete_project_bd(id)
        except Exception as e:
            internal_server_error_exception(e)
        return {"detail": "Proyecto eliminado correctamente."}