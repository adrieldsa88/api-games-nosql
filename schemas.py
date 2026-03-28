from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    nome: str
    email: str
    senha: str
    
class UsuarioLogin(BaseModel):
    email: str
    senha: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    msg: Optional[str] = None

class Jogo(BaseModel):
    titulo: str
    genero: Optional[str] = None
    desenvolvedor: Optional[str] = None
    plataforma: Optional[str] = None
    data_lancamento: Optional[str] = None

class JogoUpdate(BaseModel):
    genero: Optional[str] = None
    desenvolvedor: Optional[str] = None
    plataforma: Optional[str] = None
    data_lancamento: Optional[str] = None

class Avaliacao(BaseModel):
    titulo_jogo: str
    email_usuario: str
    nota: float
    review: str