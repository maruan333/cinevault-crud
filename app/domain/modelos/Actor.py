from pydantic import BaseModel, Field


class Actor(BaseModel):
    id: int
    nombre: str
    nacionalidad: str


class ActorCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    nacionalidad: str = Field(min_length=2, max_length=80)
