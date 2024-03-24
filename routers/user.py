from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from jwt_manager import create_token

user_router = APIRouter()

#model v1
class User(BaseModel):
    email: str
    password: str
    
    class Config:
        json_schema_extra = {
		"example" : {
				"email": 'admin@gmail.com',
				"password": "admin",
			}
		}

@user_router.post('/login', tags=['auth'])
def login(user: User):
    token = ''
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)