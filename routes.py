from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List

from database import colecao_jogos
from schemas import Jogo, JogoUpdate
from utils import serializar_jogo

router = APIRouter(prefix="/api/jogos", tags=["Jogos"])


@router.post("/", status_code=201)
def inserir_jogo(jogo: Jogo):
    """(C) Inserir um novo jogo."""

    novo_jogo = jogo.model_dump()

    if colecao_jogos.find_one({"titulo": jogo.titulo}):
        raise HTTPException(400, f"Jogo '{jogo.titulo}' já existe")

    colecao_jogos.insert_one(novo_jogo)

    return {"mensagem": f"Jogo '{jogo.titulo}' inserido"}


@router.get("/", response_model=List[dict])
def listar_ou_filtrar_jogos(
    titulo: Optional[str] = Query(None),
    genero: Optional[str] = Query(None),
    nota_minima: Optional[float] = Query(None),
    ano_minimo: Optional[int] = Query(None)
):
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
        raise HTTPException(404, "Nenhum jogo encontrado")

    return [serializar_jogo(j) for j in jogos]


@router.patch("/{titulo}")
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


@router.delete("/{titulo}")
def deletar_jogo(titulo: str):
    """(D) Deletar um jogo buscando pelo seu título."""

    resultado = colecao_jogos.delete_one({"titulo": titulo})

    if resultado.deleted_count == 0:
        raise HTTPException(404, f"Jogo '{titulo}' não encontrado")

    return {"mensagem": f"Jogo '{titulo}' deletado"}