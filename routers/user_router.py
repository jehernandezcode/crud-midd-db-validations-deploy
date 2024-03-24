from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.user_schema import User
user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    token = ''
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)