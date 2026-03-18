from fastapi import APIRouter, HTTPException, status
from typing import List
from database import colecao_avaliacoes, colecao_jogos, colecao_usuarios
from schemas import Avaliacao
from utils import serializar_avaliacao, get_data_atual
from bson import ObjectId


router = APIRouter(prefix="/api/avaliacoes", tags=["Avaliações"])


def atualizar_media_jogo(titulo_jogo: str):
    """Recalcula a média de avaliações de um jogo."""
    
    avaliacoes = list(colecao_avaliacoes.find({"titulo_jogo": titulo_jogo}))
    
    if avaliacoes:
        media = sum([a["nota"] for a in avaliacoes]) / len(avaliacoes)
        colecao_jogos.update_one(
            {"titulo": titulo_jogo},
            {"$set": {
                "media_avaliacoes": round(media, 2),
                "total_avaliacoes": len(avaliacoes)
            }}
        )
    else:
        colecao_jogos.update_one(
            {"titulo": titulo_jogo},
            {"$set": {
                "media_avaliacoes": 0.0,
                "total_avaliacoes": 0
            }}
        )


@router.post("/", status_code=201)
def criar_avaliacao(avaliacao: Avaliacao):
    """(C) Criar uma nova avaliação de jogo."""
    
    # Validar se o jogo existe
    jogo = colecao_jogos.find_one({"titulo": avaliacao.titulo_jogo})
    if not jogo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Jogo '{avaliacao.titulo_jogo}' não encontrado"
        )
    
    # Validar nota entre 0 e 10
    if avaliacao.nota < 0 or avaliacao.nota > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nota deve estar entre 0 e 10"
        )
    
    # Buscar usuário
    usuario = colecao_usuarios.find_one({"email": avaliacao.email_usuario})
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com email '{avaliacao.email_usuario}' não encontrado"
        )
    
    nova_avaliacao = {
        "titulo_jogo": avaliacao.titulo_jogo,
        "nome_usuario": usuario["nome"],
        "email_usuario": avaliacao.email_usuario,
        "nota": avaliacao.nota,
        "review": avaliacao.review,
        "data_criacao": get_data_atual()
    }
    
    resultado = colecao_avaliacoes.insert_one(nova_avaliacao)
    
    # Atualizar média de avaliações do jogo
    atualizar_media_jogo(avaliacao.titulo_jogo)
    
    return {
        "mensagem": f"Avaliação criada com sucesso!",
        "id": str(resultado.inserted_id)
    }


@router.get("/jogo/{titulo_jogo}", response_model=List[dict])
def listar_avaliacoes_jogo(titulo_jogo: str):
    """(R) Listar todas as avaliações de um jogo."""
    
    avaliacoes = list(colecao_avaliacoes.find({"titulo_jogo": titulo_jogo}).sort("data_criacao", -1))
    
    if not avaliacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma avaliação encontrada para '{titulo_jogo}'"
        )
    
    return [serializar_avaliacao(a) for a in avaliacoes]


@router.get("/usuario/{email_usuario}", response_model=List[dict])
def listar_avaliacoes_usuario(email_usuario: str):
    """(R) Listar todas as avaliações de um usuário."""
    
    avaliacoes = list(colecao_avaliacoes.find({"email_usuario": email_usuario}).sort("data_criacao", -1))
    
    if not avaliacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma avaliação encontrada para o usuário '{email_usuario}'"
        )
    
    return [serializar_avaliacao(a) for a in avaliacoes]


@router.get("/{id_avaliacao}")
def obter_avaliacao(id_avaliacao: str):
    """(R) Obter uma avaliação específica."""
    
    try:
        avaliacao = colecao_avaliacoes.find_one({"_id": ObjectId(id_avaliacao)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de avaliação inválido"
        )
    
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada"
        )
    
    return serializar_avaliacao(avaliacao)


@router.delete("/{id_avaliacao}")
def deletar_avaliacao(id_avaliacao: str):
    """(D) Deletar uma avaliação."""
    
    try:
        obj_id = ObjectId(id_avaliacao)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de avaliação inválido"
        )
    
    avaliacao = colecao_avaliacoes.find_one({"_id": obj_id})
    
    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada"
        )
    
    colecao_avaliacoes.delete_one({"_id": obj_id})
    
    # Atualizar média do jogo
    atualizar_media_jogo(avaliacao["titulo_jogo"])
    
    return {"mensagem": "Avaliação deletada com sucesso!"}
