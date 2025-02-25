from fastapi import HTTPException, status
from src.database.querys.tasks import get_one_task_by_title_bd, get_one_task_bd
from src.schemas.task import Task, TaskCreate
from src.schemas.project import Project
from src.database.querys.users import get_one_user_bd
from src.database.querys.projects import get_one_project_bd


def internal_server_error_exception(e: Exception):
    ''' Imprime un error en la consola y lanza un status 505 Internal Server Error.
    
    Args:
        e (Exception): Es un error capturado en un bloque try.
    '''
    print(f"Error: {e}") 
    raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor."
        )


def validate_task_before_creating(task_data: TaskCreate) -> None:
    ''' Valida que el título de una tarea no sea igual a otra y
    verifica si el ID del proyecto al que se le asocia existe
    dentro de la base de datos.

    Args:
        task_data (TaskCreate): Es el objeto con los datos de la tarea

    Returns:
        None
    '''
    try:
        # Se intenta realizar las consultas a la base de datos
        stored_task_title = get_one_task_by_title_bd(task_data.title)
        stored_project = get_one_project_bd(task_data.project_id)
    except Exception as e: # Si ocurre un error en la consulta anterior se captura en este bloque
        internal_server_error_exception(e)

    # Los if están fuera del try para mostrar correctamente los HTTPException al frontend
    if stored_task_title: # Si en la consulta no se obtiene ninguna tarea, se lanza un error
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Ya existe una tarea con ese título en la base de datos."
        )
    
    if not stored_project: # Si en la consulta no se obtiene ningún proyecto, se lanza un error
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontró el id del proyecto al que pertenece la tarea."
        )
   
    
def search_task(id: int) -> Task:
    ''' Busca una tarea existente en la base de datos.
    
    Args:
        id (int): El ID de la tarea

    Returns:
        Task: Es la tarea en formato JSON
    '''
    try:
        # Se intenta obtener la tarea que el usuario busca en la base de datos
        stored_task = get_one_task_bd(id) 
    except Exception as e: # Si ocurre un error en la consulta anterior se captura en este bloque
        internal_server_error_exception(e)

    if not stored_task: # Si en la consulta no se obtiene ninguna tarea, se lanza un error
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontró la tarea."
        )
    
    # Si todo sale bien se retorna la tarea
    return stored_task


def search_user(id: int):
    ''' Busca un usuario existente en la base de datos.
    
    Args:
        id (int): El ID del usuario

    Returns:
        dict: Información del usuario en formato JSON
    '''
    try:
        # Se intenta obtener el usuario que se busca en la base de datos
        stored_user = get_one_user_bd(id) 
    except Exception as e: # Si ocurre un error en la consulta anterior se captura en este bloque
        internal_server_error_exception(e)

    if not stored_user: # Si en la consulta no se obtiene ningún usuario, se lanza un error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el usuario."
        )
    
    # Si todo sale bien se retorna el usuario
    return stored_user


def search_project(id: int) -> Project:
    ''' Busca un proyecto existente en la base de datos.
    
    Args:
        id (int): El ID del proyecto

    Returns:
        Project: El proyecto en formato JSON
    '''
    try:
        stored_project = get_one_project_bd(id)
    except Exception as e:
        internal_server_error_exception(e)

    if not stored_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el proyecto."
        )
    
    return stored_project