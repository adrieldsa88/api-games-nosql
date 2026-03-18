"""
Script para popular o banco de dados MongoDB com dados de exemplo
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
url = os.getenv("DB_URL", "mongodb://localhost:27017")

# Conectar ao MongoDB
client = MongoClient(url, serverSelectionTimeoutMS=5000)
client.admin.command("ping")

db = client["sistema_avaliacoes_jogos"]
colecao_usuarios = db["usuarios"]
colecao_jogos = db["jogos"]
colecao_avaliacoes = db["avaliacoes"]

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Limpar
colecao_usuarios.delete_many({})
colecao_jogos.delete_many({})
colecao_avaliacoes.delete_many({})

# Usuários
usuarios = [
    {"nome": "João Silva", "email": "joao@example.com", "data_criacao": get_time()},
    {"nome": "Maria Santos", "email": "maria@example.com", "data_criacao": get_time()},
    {"nome": "Pedro Costa", "email": "pedro@example.com", "data_criacao": get_time()},
    {"nome": "Ana Oliveira", "email": "ana@example.com", "data_criacao": get_time()},
    {"nome": "Carlos Ferreira", "email": "carlos@example.com", "data_criacao": get_time()}
]
colecao_usuarios.insert_many(usuarios)

# Jogos
jogos = [
    {"titulo": "Elden Ring", "genero": "Action RPG", "desenvolvedor": "FromSoftware", 
     "plataforma": "Multi-platform", "data_lancamento": "2022-02-25", 
     "media_avaliacoes": 0.0, "total_avaliacoes": 0, "data_criacao": get_time()},
    {"titulo": "The Legend of Zelda: Breath of the Wild", "genero": "Adventure", 
     "desenvolvedor": "Nintendo", "plataforma": "Nintendo Switch", 
     "data_lancamento": "2017-03-03", "media_avaliacoes": 0.0, 
     "total_avaliacoes": 0, "data_criacao": get_time()},
    {"titulo": "Cyberpunk 2077", "genero": "Action RPG", "desenvolvedor": "CD Projekt Red", 
     "plataforma": "Multi-platform", "data_lancamento": "2020-12-10", 
     "media_avaliacoes": 0.0, "total_avaliacoes": 0, "data_criacao": get_time()},
    {"titulo": "Hogwarts Legacy", "genero": "Action RPG", "desenvolvedor": "Avalanche Software", 
     "plataforma": "Multi-platform", "data_lancamento": "2023-02-10", 
     "media_avaliacoes": 0.0, "total_avaliacoes": 0, "data_criacao": get_time()},
    {"titulo": "Starfield", "genero": "Action RPG", "desenvolvedor": "Bethesda Game Studios", 
     "plataforma": "Xbox/PC", "data_lancamento": "2023-09-06", 
     "media_avaliacoes": 0.0, "total_avaliacoes": 0, "data_criacao": get_time()},
    {"titulo": "Baldur's Gate 3", "genero": "RPG", "desenvolvedor": "Larian Studios", 
     "plataforma": "Multi-platform", "data_lancamento": "2023-08-03", 
     "media_avaliacoes": 0.0, "total_avaliacoes": 0, "data_criacao": get_time()},
    {"titulo": "The Witcher 3", "genero": "Action RPG", "desenvolvedor": "CD Projekt Red", 
     "plataforma": "Multi-platform", "data_lancamento": "2015-05-19", 
     "media_avaliacoes": 0.0, "total_avaliacoes": 0, "data_criacao": get_time()}
]
colecao_jogos.insert_many(jogos)

# Avaliações
avaliacoes = [
    {"titulo_jogo": "Elden Ring", "nome_usuario": "João Silva", "email_usuario": "joao@example.com", 
     "nota": 9.5, "review": "Jogo absolutamente incrível!", "data_criacao": get_time()},
    {"titulo_jogo": "Elden Ring", "nome_usuario": "Maria Santos", "email_usuario": "maria@example.com", 
     "nota": 9.0, "review": "Masterpiece! Desafiador mas justo.", "data_criacao": get_time()},
    {"titulo_jogo": "Elden Ring", "nome_usuario": "Pedro Costa", "email_usuario": "pedro@example.com", 
     "nota": 10.0, "review": "Melhor jogo que já joguei!", "data_criacao": get_time()},
    {"titulo_jogo": "The Legend of Zelda: Breath of the Wild", "nome_usuario": "Ana Oliveira", 
     "email_usuario": "ana@example.com", "nota": 9.8, "review": "Revolucionário!", "data_criacao": get_time()},
    {"titulo_jogo": "The Legend of Zelda: Breath of the Wild", "nome_usuario": "Carlos Ferreira", 
     "email_usuario": "carlos@example.com", "nota": 9.5, "review": "Liberdade total ao jogar.", "data_criacao": get_time()},
    {"titulo_jogo": "Cyberpunk 2077", "nome_usuario": "João Silva", "email_usuario": "joao@example.com", 
     "nota": 7.5, "review": "Bom jogo, mas teve problemas.", "data_criacao": get_time()},
    {"titulo_jogo": "Cyberpunk 2077", "nome_usuario": "Maria Santos", "email_usuario": "maria@example.com", 
     "nota": 8.0, "review": "Historia imersiva e mundo incrível.", "data_criacao": get_time()},
    {"titulo_jogo": "Hogwarts Legacy", "nome_usuario": "Pedro Costa", "email_usuario": "pedro@example.com", 
     "nota": 8.5, "review": "Para fãs de Harry Potter é perfeito!", "data_criacao": get_time()},
    {"titulo_jogo": "Starfield", "nome_usuario": "Ana Oliveira", "email_usuario": "ana@example.com", 
     "nota": 8.0, "review": "Ambicioso e impressionante.", "data_criacao": get_time()},
    {"titulo_jogo": "Baldur's Gate 3", "nome_usuario": "Carlos Ferreira", "email_usuario": "carlos@example.com", 
     "nota": 9.5, "review": "Épico! Profundidade roleplaying incomparável.", "data_criacao": get_time()},
    {"titulo_jogo": "The Witcher 3", "nome_usuario": "João Silva", "email_usuario": "joao@example.com", 
     "nota": 9.0, "review": "Clássico absoluto!", "data_criacao": get_time()},
    {"titulo_jogo": "The Witcher 3", "nome_usuario": "Maria Santos", "email_usuario": "maria@example.com", 
     "nota": 9.0, "review": "Geralt é incrível.", "data_criacao": get_time()}
]
colecao_avaliacoes.insert_many(avaliacoes)

# Atualizar médias
for titulo in [j["titulo"] for j in jogos]:
    avaliacoes_jogo = list(colecao_avaliacoes.find({"titulo_jogo": titulo}))
    if avaliacoes_jogo:
        media = sum([a["nota"] for a in avaliacoes_jogo]) / len(avaliacoes_jogo)
        colecao_jogos.update_one(
            {"titulo": titulo},
            {"$set": {"media_avaliacoes": round(media, 2), "total_avaliacoes": len(avaliacoes_jogo)}}
        )

print("Database populated: 5 users, 7 games, 12 reviews")
client.close()
