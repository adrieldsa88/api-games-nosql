from pydantic import BaseModel
from typing import Optional

class Jogo(BaseModel):
    titulo: str
    genero: Optional[str] = None
    ano: Optional[int] = None
    nota: Optional[float] = None


class JogoUpdate(BaseModel):
    genero: Optional[str] = None
    ano: Optional[int] = None
    nota: Optional[float] = None