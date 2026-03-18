from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from database import colecao_jogos, colecao_avaliacoes
from schemas import Jogo, JogoUpdate
from utils import serializar_jogo, serializar_avaliacao, get_data_atual


router = APIRouter(prefix="/api/jogos", tags=["Jogos"])


@router.post("/", status_code=201)
def inserir_jogo(jogo: Jogo):
    """(C) Inserir um novo jogo."""
    
    if colecao_jogos.find_one({"titulo": jogo.titulo}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Jogo '{jogo.titulo}' já existe"
        )
    
    novo_jogo = jogo.model_dump()
    novo_jogo["data_criacao"] = get_data_atual()
    novo_jogo["media_avaliacoes"] = 0.0
    novo_jogo["total_avaliacoes"] = 0
    
    resultado = colecao_jogos.insert_one(novo_jogo)
    
    return {
        "mensagem": f"Jogo '{jogo.titulo}' inserido com sucesso!",
        "id": str(resultado.inserted_id)
    }


@router.get("/", response_model=List[dict])
def listar_jogos(
    titulo: Optional[str] = Query(None),
    genero: Optional[str] = Query(None),
    desenvolvedor: Optional[str] = Query(None),
    plataforma: Optional[str] = Query(None)
):
    """(R) Listar todos os jogos com filtros opcionais."""
    
    query = {}
    
    if titulo:
        query["titulo"] = {"$regex": titulo, "$options": "i"}
    if genero:
        query["genero"] = {"$regex": genero, "$options": "i"}
    if desenvolvedor:
        query["desenvolvedor"] = {"$regex": desenvolvedor, "$options": "i"}
    if plataforma:
        query["plataforma"] = {"$regex": plataforma, "$options": "i"}
    
    jogos = list(colecao_jogos.find(query).sort("media_avaliacoes", -1))
    
    if not jogos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum jogo encontrado"
        )
    
    return [serializar_jogo(j) for j in jogos]


@router.get("/{titulo}")
def obter_jogo(titulo: str):
    """(R) Obter detalhes de um jogo específico."""
    
    jogo = colecao_jogos.find_one({"titulo": titulo})
    
    if not jogo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogo '{titulo}' não encontrado"
        )
    
    # Buscar avaliações do jogo
    avaliacoes = list(colecao_avaliacoes.find({"titulo_jogo": titulo}))
    
    jogo_detalhes = serializar_jogo(jogo)
    jogo_detalhes["avaliacoes"] = [serializar_avaliacao(a) for a in avaliacoes]
    
    return jogo_detalhes


@router.patch("/{titulo}")
def atualizar_jogo(titulo: str, jogo_update: JogoUpdate):
    """(U) Atualizar dados de um jogo."""
    
    atualizacoes = jogo_update.model_dump(exclude_unset=True)
    
    if not atualizacoes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum dado para atualizar"
        )
    
    resultado = colecao_jogos.update_one({"titulo": titulo}, {"$set": atualizacoes})
    
    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogo '{titulo}' não encontrado"
        )
    
    return {"mensagem": f"Jogo '{titulo}' atualizado com sucesso!"}


@router.delete("/{titulo}")
def deletar_jogo(titulo: str):
    """(D) Deletar um jogo."""
    
    # Deletar também as avaliações do jogo
    colecao_avaliacoes.delete_many({"titulo_jogo": titulo})
    
    resultado = colecao_jogos.delete_one({"titulo": titulo})
    
    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogo '{titulo}' não encontrado"
        )
    
    return {"mensagem": f"Jogo '{titulo}' e suas avaliações foram deletados"}
