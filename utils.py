from datetime import datetime
from bson import ObjectId

def serializar_documento(doc):
    """Converte ObjectId para string"""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def serializar_jogo(jogo):
    """Serializa documento de jogo"""
    return serializar_documento(jogo)

def serializar_avaliacao(avaliacao):
    """Serializa documento de avaliação"""
    return serializar_documento(avaliacao)

def serializar_usuario(usuario):
    """Serializa documento de usuário"""
    return serializar_documento(usuario)

def get_data_atual():
    """Retorna a data/hora atual formatada"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")