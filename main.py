from fastapi import FastAPI
from fastapi.responses import JSONResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie_router import movie_router
from routers.user_router import user_router

#metadata Api
app = FastAPI()
app.title = 'app with fastapi'
app.version = '0.0.1'


#instanciar base de datos
Base.metadata.create_all(bind=engine)

#Add error handler middleware
app.add_middleware(ErrorHandler)

#Add router middleware
app.include_router(movie_router)
app.include_router(user_router)

#Mock static
movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 3,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Drama"
	}
    ]

#routes
@app.get('/', tags=['home'])
def message():
    return JSONResponse(content='hello')

