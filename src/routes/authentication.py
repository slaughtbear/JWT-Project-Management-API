# Manipulación de archivos
import os

# Tipos de datos
from typing import Annotated, Dict

# Librería para trabajar con Jason Web Tokens
import jwt

# Librería para encriptación de contraseñas
from passlib.context import CryptContext

# Manipulación de variables de entorno
from dotenv import load_dotenv

# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Esquemas Pydantic
from src.schemas.users import User, UserCreate

# Base de datos
from src.database.querys.users import create_user_bd, get_one_user_by_username_bd

# Funciones Auxiliares
from src.utils.functions import internal_server_error_exception


auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login")

"""
CryptContext es una clase de passlib que permite manejar diferentes esquemas de encriptación.
Se realiza una instancia de la clase y se define el esquema de encriptación,
en este caso el esquema es "bycrypt"
"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")


def encode_token(payload: Dict) -> str:
    ''' Genera un token a partir de la información del usuario.
    
    Args:
        payload (Dict): Diccionario con los datos del usuario.

    Returns:
        str: El token generado para el usuario.
    '''
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Dict:
    ''' Decodifica un token y retorna la información del usuario.
    
    Args:
        token (str): El token del usuario.

    Returns:
        Dict: Diccionario con la información del usuario.
    '''
    data = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    user = get_one_user_by_username_bd(data["username"])
    return user


def get_password_hash(password: str) -> str:
    """ Recibe una contraseña en texto plano y la encripta.

    Args:
        password (str): Contraseña en texto plano.

    Returns:
        str: La contraseña encriptada.

    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Compara una contraseña en texto plano con la contraseña con hash, verifica que coincidan, si es así se retorna True.

    Args:
        plain_password (str): Contraseña en texto plano.
        hashed_password (str): Contraseña con hash.

    Returns:
        bool: True si coinciden, False si no coinciden.
    """
    return pwd_context.verify(plain_password, hashed_password)


@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Dict[str, str]:
    """ Endpoint para iniciar sesión.
    
    Args:
        form_data: Dependencia que extrae el "username" y "password" de un formulario enviado por el frontend.
    
    Returns:
        Dict[str, str]: Token con los datos del usuario.
    """
    try:
        user = get_one_user_by_username_bd(form_data.username)
    except IndexError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "El usuario no existe en la base de datos."
        )
    except Exception as e:
        internal_server_error_exception(e)

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Las contraseñas no coinciden."
        )

    token = encode_token({
                "username": user["username"],
                "email": user["email"],
            })
    
    return {"access_token": token}


@auth_router.post("/register", response_model=User)
async def register(user_data: UserCreate) -> User:
    """Endpoint para agregar un usuario.

    Args:
        user_data (UserCreate): Datos del usuario bajo el esquema Pydantic
        para crear un usuario.

    Returns:
    """

    # Encriptar la contraseña antes de guardarla
    hashed_password = get_password_hash(user_data.password)
    user_data.password = hashed_password

    try:
        return create_user_bd(user_data)
    except Exception as e:
        internal_server_error_exception(e)
