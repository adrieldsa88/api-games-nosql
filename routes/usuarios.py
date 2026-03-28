from fastapi import APIRouter, HTTPException, status
from typing import List
from database import colecao_usuarios, colecao_avaliacoes
from schemas import Usuario
from utils import serializar_usuario, serializar_avaliacao, get_data_atual
from auth import criar_token_acesso, verificar_token_acesso, hash_senha, verificar_senha


router = APIRouter(prefix="/api/usuarios", tags=["Usuários"])


@router.post("/", status_code=201)
async def registrar_usuario(usuario: Usuario):
    """(C) Criar um novo usuário."""
    
    if colecao_usuarios.find_one({"email": usuario.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Usuário com email '{usuario.email}' já existe"
        )
    senha_criptografada = hash_senha(usuario.senha)
    
    novo_usuario = {
        "nome": usuario.nome,
        "email": usuario.email,
        "senha": senha_criptografada,
        "data_criacao": get_data_atual()
    }
    
    resultado = colecao_usuarios.insert_one(novo_usuario)
    
    return {
        "mensagem": f"Usuário '{usuario.nome}' criado com sucesso!",
        "id": str(resultado.inserted_id)
    }
    
@router.post("/login", response_model=dict)
async def login_usuario(usuario: Usuario):
    """Autenticar usuário e gerar token de acesso."""
    
    usuario_db = colecao_usuarios.find_one({"email": usuario.email})
    
    if not usuario_db or not verificar_senha(usuario.senha, usuario_db["senha"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos"
        )
    
    token_acesso = criar_token_acesso({"sub": usuario.email})
    
    return {
        "access_token": token_acesso,
        "token_type": "bearer",
        "msg": "Login bem-sucedido"
    }


@router.get("/", response_model=List[dict])
async def listar_usuarios():
    """(R) Listar todos os usuários."""
    
    usuarios = list(colecao_usuarios.find())
    
    if not usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum usuário encontrado"
        )
    
    return [serializar_usuario(u) for u in usuarios]


@router.get("/{email}", response_model=dict)
async def obter_usuario(email: str):
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
async def deletar_usuario(email: str):
    """(D) Deletar um usuário."""
    
    # Deletar também as avaliações do usuário
    colecao_avaliacoes.delete_many({"email_usuario": email})

    resultado = colecao_usuarios.delete_one({"email": email})

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com email '{email}' não encontrado"
        )

    return {"mensagem": "Usuário e suas avaliações foram deletados"}
