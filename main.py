from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from pymongo import MongoClient
import os
from dotenv import load_dotenv 
load_dotenv()
url = os.getenv("DB_URL")

try:
    client = MongoClient(url, serverSelectionTimeoutMS=5000)
    db = client["projeto_banco_de_dados"]
    colecao_jogos = db["jogos"]
    client.admin.command('ping')
    print("Conexão com o MongoDB estabelecida com sucesso!")
except Exception as e:
    print(f"Erro crítico ao conectar ao banco de dados: {e}")
    exit()

app = FastAPI(
    title="Gerenciador de Jogos NoSQL",
    description="API feita com FastAPI para gerenciar a coleção de jogos no MongoDB.",
    version="1.0.1"
)

class Jogo(BaseModel):
    titulo: str
    genero: Optional[str] = None
    ano: Optional[int] = None
    nota: Optional[float] = None

class JogoUpdate(BaseModel):
    genero: Optional[str] = None
    ano: Optional[int] = None
    nota: Optional[float] = None

def serializar_jogo(jogo_db) -> dict:
    if jogo_db:
        jogo_db["_id"] = str(jogo_db["_id"])
    return jogo_db


@app.post("/api/jogos/", response_model=dict, status_code=201)
def inserir_jogo(jogo: Jogo):
    """(C) Inserir um novo jogo."""
    novo_jogo = jogo.model_dump()
    colecao_jogos.insert_one(novo_jogo)
    return {"mensagem": f"Sucesso: Jogo '{jogo.titulo}' inserido no banco!"}

@app.get("/api/jogos/", response_model=List[dict])
def listar_ou_filtrar_jogos(
    titulo: Optional[str] = Query(None, description="Buscar por parte do título"),
    genero: Optional[str] = Query(None, description="Filtrar por gênero"),
    nota_minima: Optional[float] = Query(None, description="Filtrar por nota mínima"),
    ano_minimo: Optional[int] = Query(None, description="Filtrar por ano mínimo")
):
    # sourcery skip: reintroduce-else, swap-if-else-branches, use-named-expression
    """
    (R) Listar Tudo e Filtros Combinados.
    Se nenhum parâmetro for passado, lista todos os jogos.
    Se parâmetros forem passados, atua como um filtro personalizado.
    """
    query = {}
    
    if titulo:
        query["titulo"] = {"$regex": titulo, "$options": "i"}
    if genero:
        query["genero"] = {"$regex": genero, "$options": "i"}
    if nota_minima is not None:
        query["nota"] = {"$gte": nota_minima}
    if ano_minimo is not None:
        query["ano"] = {"$gte": ano_minimo}

    jogos = list(colecao_jogos.find(query).sort("nota", -1))
    
    if not jogos:
        raise HTTPException(status_code=404, detail="Nenhum jogo encontrado com os critérios fornecidos.")
    
    return [serializar_jogo(j) for j in jogos]

@app.patch("/api/jogos/{titulo}")
def atualizar_jogo(titulo: str, jogo_update: JogoUpdate):
    """
    (U) Atualizar dados de um jogo. 
    Se enviar um campo, ele atualiza. Se omitir ou enviar null, ele ignora.
    """
    dados_enviados = jogo_update.model_dump(exclude_unset=True)
    
    atualizacoes = {k: v for k, v in dados_enviados.items() if v is not None}
    
    if not atualizacoes:
        raise HTTPException(
            status_code=400, 
            detail="Nenhum dado válido foi enviado. Informe gênero, ano ou nota para atualizar."
        )

    resultado = colecao_jogos.update_one({"titulo": titulo}, {"$set": atualizacoes})
    
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Jogo '{titulo}' não encontrado no banco.")
        
    if resultado.modified_count == 0:
        return {"mensagem": f"Aviso: Jogo '{titulo}' encontrado, mas os dados enviados já eram iguais aos atuais."}

    return {"mensagem": f"Sucesso: Jogo '{titulo}' atualizado com sucesso!"}

@app.delete("/api/jogos/{titulo}")
def deletar_jogo(titulo: str):
    """(D) Deletar um jogo buscando pelo seu título."""
    resultado = colecao_jogos.delete_one({"titulo": titulo})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Aviso: Jogo '{titulo}' não encontrado.")
        
    return {"mensagem": f"Sucesso: Jogo '{titulo}' deletado!"}