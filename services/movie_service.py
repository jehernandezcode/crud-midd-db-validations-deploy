from models.movie import MovieDB

class MovieService():
    
    def __init__(self, db) -> None:
        self.db = db
        
        
    def getMovies(self):
        return self.db.query(MovieDB).all()
    
    def getMoviesById(self, id):
        return self.db.query(MovieDB).filter(MovieDB.id == id).first()
    
    def getMoviesByCategory(self, category):
        return self.db.query(MovieDB).filter(MovieDB.category == category).all()