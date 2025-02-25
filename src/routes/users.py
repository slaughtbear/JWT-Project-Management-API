from fastapi import APIRouter, Path, HTTPException, status
from typing import List, Dict
from src.schemas.users import User, UserCreate, UserUpdate
from src.database.querys.users import get_all_users_bd, create_user_bd, update_user_bd, delete_user_bd
from src.utils.functions import internal_server_error_exception, search_user


users_router = APIRouter()


@users_router.get("/", response_model=List[User])
async def get_users() -> List[User]:
    """Endpoint para obtener todos los usuarios."""
    try:
        users = get_all_users_bd()
    except Exception as e:
        internal_server_error_exception(e)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró ningún usuario..."
        )
    
    return users


@users_router.get("/{id}", response_model=User)
async def get_user_by_id(id: int = Path(gt=0)) -> User:
    """Endpoint para obtener un usuario por ID."""
    return search_user(id)


@users_router.post("/", response_model=User)
async def add_user(user_data: UserCreate) -> User:
    """Endpoint para agregar un usuario."""
    try:
        return create_user_bd(user_data)
    except Exception as e:
        internal_server_error_exception(e)


@users_router.put("/{id}", response_model=User)
async def update_user(user_data: UserUpdate, id: int = Path(gt=0)) -> User:
    """Endpoint para actualizar un usuario."""
    if search_user(id):
        try:
            return update_user_bd(user_data, id)
        except Exception as e:
            internal_server_error_exception(e)


@users_router.delete("/{id}", response_model=Dict[str, str])
async def delete_user(id: int = Path(gt=0)) -> Dict[str, str]:
    """Endpoint para eliminar un usuario."""
    if search_user(id):
        try:
            delete_user_bd(id)
        except Exception as e:
            internal_server_error_exception(e)
        return {"detail": "Usuario eliminado correctamente."}
