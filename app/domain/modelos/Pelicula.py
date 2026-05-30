from typing import Optional
from pydantic import BaseModel, Field


class Pelicula(BaseModel):
    id: int
    titulo: str
    anio: int
    director: str
    sinopsis: str
    poster_url: Optional[str] = None


class PeliculaCreate(BaseModel):
    titulo: str = Field(min_length=2, max_length=120)
    anio: int = Field(ge=1888, le=2100)
    director: str = Field(min_length=2, max_length=120)
    sinopsis: str = Field(min_length=10, max_length=600)
    poster_url: Optional[str] = Field(default=None, max_length=255)


class PeliculaUpdate(PeliculaCreate):
    pass
