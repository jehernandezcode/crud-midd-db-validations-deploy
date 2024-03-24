from models.movie import MovieDB
from fastapi.responses import JSONResponse

class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db
        
        
    def getMovies(self):
        return self.db.query(MovieDB).all()
    
    def getMoviesById(self, id):
        return self.db.query(MovieDB).filter(MovieDB.id == id).first()
    
    def getMoviesByCategory(self, category):
        return self.db.query(MovieDB).filter(MovieDB.category == category).all()
    
    def addMovie(self, movie: MovieDB) -> None:
        new_movie = MovieDB(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def updateMovie(self, id:  int, movie: MovieDB) -> None:
        movieQuery = self.db.query(MovieDB).filter(MovieDB.id == id).first()
        
        movieQuery.title= movie.title
        movieQuery.overview = movie.overview
        movieQuery.year = movie.year
        movieQuery.rating = movie.rating
        movieQuery.category = movie.category
        self.db.commit()
        return
    
    def deleteMovie(self, movieQuery: MovieDB) -> None:
        self.db.delete(movieQuery)
        self.db.commit()
        return