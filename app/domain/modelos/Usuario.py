from pydantic import BaseModel, Field


class Usuario(BaseModel):
    id: int
    username: str
    es_admin: bool


class UsuarioCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=80)
    es_admin: bool = False
