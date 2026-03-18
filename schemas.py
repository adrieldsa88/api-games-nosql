from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    nome: str
    email: str

class Jogo(BaseModel):
    titulo: str
    genero: Optional[str] = None
    desenvolvedor: Optional[str] = None
    plataforma: Optional[str] = None
    data_lancamento: Optional[str] = None

class JogoUpdate(BaseModel):
    titulo: Optional[str] = None
    genero: Optional[str] = None
    desenvolvedor: Optional[str] = None
    plataforma: Optional[str] = None
    data_lancamento: Optional[str] = None

class Avaliacao(BaseModel):
    titulo_jogo: str
    email_usuario: str
    nota: float
    review: str