from typing import List, Dict
from fastapi import APIRouter, Path, HTTPException, status
from src.schemas.task import Task, TaskCreate, TaskUpdate
from src.database.querys.tasks import get_all_tasks_bd, create_task_bd, update_task_bd, delete_task_bd
from src.utils.functions import internal_server_error_exception, validate_task_before_creating, search_task



tasks_router = APIRouter()


@tasks_router.get("/", response_model = List[Task])
async def get_tasks() -> List[Task]:
    try:
        # Se obtienen todas las tareas de la base de datos
        tasks = get_all_tasks_bd()
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
async def get_task_by_id(id: int = Path(gt = 0)) -> Task:
    ''' Endpoint de tipo GET para obtener una tarea por ID.

    Args:
        id (int): ID de la tarea a buscar.

    Returns:
        Task: Es el objeto que contiene la tarea buscada.
    
    '''
    return search_task(id)


@tasks_router.post("/", response_model = Task)
async def add_task(task_data: TaskCreate) -> Task:
    ''' Endpoint de tipo POST para agregar tareas a la base de datos.
    
    Args:
        task_data (TaskCreate): Es el objeto JSON que el frontend envía con los datos para crear una tarea (excluyendo el "id" y "created_at" que son generados por la base de datos).

    Returns:
        Task: Es el objeto que contiene todos los datos de la tarea.
    '''

    # Se validan los datos de la tarea antes de agregarla
    validate_task_before_creating(task_data) 

    try: 
        # Se intenta crear la tarea en la base de datos y retornarla como respuesta.
        return create_task_bd(task_data)
    except Exception as e: # Si ocurre un error se captura en este bloque
        internal_server_error_exception(e)


@tasks_router.put("/{id}", response_model = Task)
async def update_task(task_data: TaskUpdate, id: int = Path(gt = 0)) -> Task:
    ''' Endpoint de tipo PUT para actualizar tareas de la base de datos.

    Args:
        task_data (TaskUpdate): Es el objeto JSON que el frontend envía con los datos para actualizar una tarea.
        id (int): Es el ID de la tarea a actualizar.

    Returns:
        Task: Es el objeto que contiene los datos actualizados de la tarea.
    '''
    if search_task(id): # Si se encuentra la tarea a actualizar
        try:
            # Se intenta actualizar la tarea en la base de datos y retornarla
            return update_task_bd(task_data, id)
        except Exception as e: # Si ocurre un error se captura en este bloque
            internal_server_error_exception(e)


@tasks_router.delete("/{id}")
async def delete_task(id: int = Path(gt = 0)) -> Dict:
    ''' Endpoint de tipo DELETE para eliminar una tarea de la base de datos.

    Args:
        id (int): Es el ID de la tarea a eliminar.

    Returns:
        Dict: Un diccionario con un mensaje para el frontend.
    '''
    if search_task(id): # Si se encuentra la tarea
        try:
            # Se intenta eliminar de la base de datos
            delete_task_bd(id)
        except Exception as e: # Si ocurre un error se captura en este bloque
            internal_server_error_exception(e)
        # Si todo sale bien se retorna un mensaje de confirmación
        return {"detail": "Tarea eliminada correctamente."}