from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from database import colecao_usuarios, colecao_jogos, colecao_avaliacoes
from schemas import Usuario, Jogo, JogoUpdate, Avaliacao
from utils import serializar_jogo, serializar_avaliacao, serializar_usuario, get_data_atual
from bson import ObjectId

# Routers
router_usuarios = APIRouter(prefix="/api/usuarios", tags=["Usuários"])
router_jogos = APIRouter(prefix="/api/jogos", tags=["Jogos"])
router_avaliacoes = APIRouter(prefix="/api/avaliacoes", tags=["Avaliações"])

# ============ ROTAS DE USUÁRIOS ============

@router_usuarios.post("/", status_code=201)
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


@router_usuarios.get("/", response_model=List[dict])
def listar_usuarios():
    """(R) Listar todos os usuários."""
    
    usuarios = list(colecao_usuarios.find())
    
    if not usuarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum usuário encontrado"
        )
    
    return [serializar_usuario(u) for u in usuarios]


@router_usuarios.get("/{email}")
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


@router_usuarios.delete("/{email}")
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


# ============ ROTAS DE JOGOS ============

@router_jogos.post("/", status_code=201)
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


@router_jogos.get("/", response_model=List[dict])
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


@router_jogos.get("/{titulo}")
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


@router_jogos.patch("/{titulo}")
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


@router_jogos.delete("/{titulo}")
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


# ============ ROTAS DE AVALIAÇÕES ============

@router_avaliacoes.post("/", status_code=201)
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


@router_avaliacoes.get("/jogo/{titulo_jogo}", response_model=List[dict])
def listar_avaliacoes_jogo(titulo_jogo: str):
    """(R) Listar todas as avaliações de um jogo."""
    
    avaliacoes = list(colecao_avaliacoes.find({"titulo_jogo": titulo_jogo}).sort("data_criacao", -1))
    
    if not avaliacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma avaliação encontrada para '{titulo_jogo}'"
        )
    
    return [serializar_avaliacao(a) for a in avaliacoes]


@router_avaliacoes.get("/usuario/{email_usuario}", response_model=List[dict])
def listar_avaliacoes_usuario(email_usuario: str):
    """(R) Listar todas as avaliações de um usuário."""
    
    avaliacoes = list(colecao_avaliacoes.find({"email_usuario": email_usuario}).sort("data_criacao", -1))
    
    if not avaliacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhuma avaliação encontrada para o usuário '{email_usuario}'"
        )
    
    return [serializar_avaliacao(a) for a in avaliacoes]


@router_avaliacoes.get("/{id_avaliacao}")
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


@router_avaliacoes.delete("/{id_avaliacao}")
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


# ============ FUNÇÃO AUXILIAR ============

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