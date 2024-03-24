from pydantic import BaseModel, Field
from typing import Optional

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