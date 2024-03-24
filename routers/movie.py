from fastapi import Path, Query, Depends, APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.responses import JSONResponse
from config.database import Session
from models.movie import MovieDB
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie_service import MovieService

movie_router = APIRouter()


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


@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def getMovies() -> List[Movie]:
    db = Session()
    moviesDB = MovieService(db).getMovies()
    return JSONResponse(status_code=200, content=jsonable_encoder(moviesDB))

@movie_router.get('/movies/{id}', tags=['Movies'], response_model=Movie, status_code=200)
def getMoviesById(id: int = Path(ge=0, le=2000)) -> Movie:
    db = Session()
    movie = MovieService(db).getMoviesById(id)
    if not movie: 
        return JSONResponse(status_code=404, content='Not found')
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))

@movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie], status_code=200)
def getMoviesByCategory(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    movies = MovieService(db).getMoviesByCategory(category)
    if len(movies) <= 0: 
        return JSONResponse(status_code=404, content='Not found')
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))

@movie_router.post('/movies/', tags=['Movies'], response_model=dict, status_code=201)
def addMovie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieDB(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado una pelicula"})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
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

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def deleteMovie(id: int) -> dict:
    
    db = Session()
    movieQuery = db.query(MovieDB).filter(MovieDB.id == id).first()
    if not movieQuery:
        return JSONResponse(status_code=404, content='Not found')
    
    db.delete(movieQuery)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado una pelicula"})