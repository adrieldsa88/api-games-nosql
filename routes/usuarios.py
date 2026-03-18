from fastapi import APIRouter, HTTPException, status
from typing import List
from database import colecao_usuarios, colecao_avaliacoes
from schemas import Usuario
from utils import serializar_usuario, serializar_avaliacao, get_data_atual


router = APIRouter(prefix="/api/usuarios", tags=["Usuários"])


@router.post("/", status_code=201)
def criar_usuario(usuario: Usuario):
    """(C) Criar um novo usuário."""
    
    if colecao_usuarios.find_one({"email": usuario.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Usuário com email '{usuario.email}' já existe"
        )
    
    novo_usuario = {
        "nome": usuario.nome,
        "email": usuario.email,
        "data_criacao": get_data_atual()
    }
    
    resultado = colecao_usuarios.insert_one(novo_usuario)
    
    return {
        "mensagem": f"Usuário '{usuario.nome}' criado com sucesso!",
        "id": str(resultado.inserted_id)
    }


@router.get("/", response_model=List[dict])
def listar_usuarios():
    """(R) Listar todos os usuários."""
    
    usuarios = list(colecao_usuarios.find())
    
    if not usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum usuário encontrado"
        )
    
    return [serializar_usuario(u) for u in usuarios]


@router.get("/{email}")
def obter_usuario(email: str):
    """(R) Obter detalhes de um usuário."""
    
    usuario = colecao_usuarios.find_one({"email": email})
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com email '{email}' não encontrado"
        )
    
    # Buscar avaliações do usuário
    avaliacoes = list(colecao_avaliacoes.find({"email_usuario": email}))
    
    usuario_detalhes = serializar_usuario(usuario)
    usuario_detalhes["avaliacoes"] = [serializar_avaliacao(a) for a in avaliacoes]
    
    return usuario_detalhes


@router.delete("/{email}")
def deletar_usuario(email: str):
    """(D) Deletar um usuário."""
    
    # Deletar também as avaliações do usuário
    colecao_avaliacoes.delete_many({"email_usuario": email})
    
    resultado = colecao_usuarios.delete_one({"email": email})
    
    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com email '{email}' não encontrado"
        )
    
    return {"mensagem": f"Usuário e suas avaliações foram deletados"}
