from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Dict
from dotenv import load_dotenv
import os
import jwt
from src.database.querys.users import get_one_user_by_username_bd
from src.utils.functions import internal_server_error_exception


jwt_auth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login")

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


@jwt_auth.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = get_one_user_by_username_bd(form_data.username)
    except IndexError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "El usuario no existe en la base de datos."
        )
    except Exception as e:
        internal_server_error_exception(e)

    if form_data.password != user["password"]:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Las contraseñas no coinciden."
        )

    token = encode_token({
                "username": user["username"],
                "email": user["email"],
            })
    
    return {"access_token": token}


@jwt_auth.get("/profile")
async def profile(user: Annotated[Dict, Depends(decode_token)]):
    return user
