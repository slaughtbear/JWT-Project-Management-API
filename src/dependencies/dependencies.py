from typing import Annotated, Dict
from fastapi import Depends, Path
from src.routes.authentication import decode_token

GetCurrentUser = Annotated[Dict, Depends(decode_token)]
IdValidator = Annotated[int, Path(gt=0)] 
