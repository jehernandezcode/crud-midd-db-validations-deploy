from fastapi import FastAPI, Path, Query, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.responses import JSONResponse
from config.database import Session, engine, Base
from models.movie import MovieDB
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer 
from jwt_manager import create_token

#metadata Api
app = FastAPI()
app.title = 'app with fastapi'
app.version = '0.0.1'


#instanciar base de datos
Base.metadata.create_all(bind=engine)


#Add error handler middleware
app.add_middleware(ErrorHandler)

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


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str
    year : int = Field(ge=2000)
    rating : float
    category : str
    
    class Config:
        json_schema_extra = {
		"example" : {
				"id": 1,
				"title": "Mi pelicula",
    			"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
				"year": 2009,
				"rating": 6.9,
				"category": "Acción"
			}
		}
        
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

@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def getMovies() -> List[Movie]:
    db = Session()
    moviesDB = db.query(MovieDB).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(moviesDB))

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie, status_code=200)
def getMoviesById(id: int = Path(ge=0, le=2000)) -> Movie:
    db = Session()
    movie = db.query(MovieDB).filter(MovieDB.id == id).first()
    if not movie: 
        return JSONResponse(status_code=404, content='Not found')
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))

@app.get('/movies/', tags=['Movies'], response_model=List[Movie], status_code=200)
def getMoviesByCategory(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    movies = db.query(MovieDB).filter(MovieDB.category == category).all()
    if len(movies) <= 0: 
        return JSONResponse(status_code=404, content='Not found')
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

@app.post('/movies/', tags=['Movies'], response_model=dict, status_code=201)
def addMovie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieDB(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado una pelicula"})

@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def updateMovie(id: int, movie: Movie) -> dict:
    db = Session()
    movieQuery = db.query(MovieDB).filter(MovieDB.id == id).first()
    if not movieQuery:
        return JSONResponse(status_code=404, content='Not found')
    
    movieQuery.title= movie.title
    movieQuery.overview = movie.overview
    movieQuery.year = movie.year
    movieQuery.rating = movie.rating
    movieQuery.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha actualizado una pelicula"})

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def deleteMovie(id: int) -> dict:
    
    db = Session()
    movieQuery = db.query(MovieDB).filter(MovieDB.id == id).first()
    if not movieQuery:
        return JSONResponse(status_code=404, content='Not found')
    
    db.delete(movieQuery)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado una pelicula"})

@app.post('/login', tags=['auth'])
def login(user: User):
    token = ''
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)