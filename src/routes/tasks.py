# FastAPI
from fastapi import APIRouter, HTTPException, status

# Tipos de datos
from typing import List, Dict

# Esquemas Pydantic
from src.schemas.task import Task, TaskCreate, TaskUpdate

# Base de datos
from src.database.querys.tasks import (
    get_all_tasks_bd,
    create_task_bd,
    update_task_bd,
    delete_task_bd
)

# Funciones auxiliares
from src.utils.functions import (
    internal_server_error_exception,
    validate_task_before_creating,
    search_task
)

# Dependencias
from src.dependencies.dependencies import GetCurrentUser, IdValidator


tasks_router = APIRouter()


@tasks_router.get("/", response_model = List[Task])
async def get_tasks(current_user: GetCurrentUser) -> List[Task]:
    """ Endpoint para que un usuario obtenga todas sus tareas.

    Args:
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.
    
    Returns: 
        List (Task): Lista de las tareas que le pertenecen únicamente al usuario que realiza la petición.
    """
    try:
        # Se obtienen todas las tareas de la base de datos
        tasks = get_all_tasks_bd(current_user["id"])
    except Exception as e:  # Si ocurre un error en la consulta anterior se captura en este bloque
        internal_server_error_exception(e)

    if not tasks: # Si en la consulta no se obtiene ninguna tarea, se lanza un error
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No se encontró ninguna tarea..."
        )
    
    # Si todo sale bien, se retornan todas las tareas
    return tasks


@tasks_router.get("/{id}", response_model = Task)
async def get_task_by_id(current_user: GetCurrentUser, id: IdValidator) -> Task:
    ''' Endpoint de tipo GET para obtener una tarea por ID.

    Args:
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.
        id (IdValidator): ID de la tarea a buscar.

    Returns:
        Task: Tarea registrada por el usuario y retornada bajo un esquema definido en Pydantic.
    '''
    return search_task(id, current_user["id"])


@tasks_router.post("/", response_model = Task)
async def add_task(current_user: GetCurrentUser, task_data: TaskCreate) -> Task:
    ''' Endpoint de tipo POST para agregar tareas a la base de datos.
    
    Args:
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.
        task_data (TaskCreate): Es el objeto JSON que el frontend envía con los datos para crear una tarea (excluyendo el "id" y "created_at" que son generados por la base de datos).

    Returns:
        Task: Tarea creada por el usuario y retornada bajo un esquema definido en Pydantic.
    '''

    # Se validan los datos de la tarea antes de agregarla
    validate_task_before_creating(task_data, current_user["id"]) 

    try: 
        # Se intenta crear la tarea en la base de datos y retornarla como respuesta.
        return create_task_bd(task_data, current_user)
    except Exception as e: # Si ocurre un error se captura en este bloque
        internal_server_error_exception(e)


@tasks_router.put("/{id}", response_model = Task)
async def update_task(task_data: TaskUpdate, id: IdValidator, current_user: GetCurrentUser) -> Task:
    ''' Endpoint de tipo PUT para actualizar tareas de la base de datos.

    Args:
        task_data (TaskUpdate): Es el objeto JSON que el frontend envía con los datos para actualizar una tarea.
        id (IdValidator): Es el ID de la tarea a actualizar.
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.

    Returns:
        Task: Tarea actualizada por el usuario y retornada bajo un esquema definido en Pydantic.
    '''
    if search_task(id, current_user["id"]): # Si se encuentra la tarea a actualizar
        try:
            # Se intenta actualizar la tarea en la base de datos y retornarla
            return update_task_bd(task_data, id)
        except Exception as e: # Si ocurre un error se captura en este bloque
            internal_server_error_exception(e)


@tasks_router.delete("/{id}")
async def delete_task(id: IdValidator, current_user: GetCurrentUser) -> Dict:
    ''' Endpoint de tipo DELETE para eliminar una tarea de la base de datos.

    Args:
        id (int): Es el ID de la tarea a eliminar.
        current_user (GetCurrentUser): Es la dependencia que obtiene los datos del usuario a través de un token en el header.

    Returns:
        Dict: Un diccionario con un mensaje para el frontend.
    '''
    if search_task(id, current_user["id"]): # Si se encuentra la tarea
        try:
            # Se intenta eliminar de la base de datos
            delete_task_bd(id)
        except Exception as e: # Si ocurre un error se captura en este bloque
            internal_server_error_exception(e)
        # Si todo sale bien se retorna un mensaje de confirmación
        return {"detail": "Tarea eliminada correctamente."}