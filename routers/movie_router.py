from fastapi import Path, Query, Depends, APIRouter
from typing import List
from fastapi.responses import JSONResponse
from config.database import Session
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie_service import MovieService
from schemas.movie_schema import Movie

movie_router = APIRouter()


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
    MovieService(db).addMovie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado una pelicula"})

@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def updateMovie(id: int, movie: Movie) -> dict:
    db = Session()
    movieQuery = MovieService(db).getMoviesById(id)
    if not movieQuery:
        return JSONResponse(status_code=404, content='Not found')
    MovieService(db).updateMovie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha actualizado una pelicula"})

@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def deleteMovie(id: int) -> dict:
    db = Session()
    movieQuery = MovieService(db).getMoviesById(id)
    
    if not movieQuery:
        return JSONResponse(status_code=404, content='Not found')
        
    MovieService(db).deleteMovie(movieQuery)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado una pelicula"})