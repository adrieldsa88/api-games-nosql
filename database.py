from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DB_URL")

client = MongoClient(url, serverSelectionTimeoutMS=5000)

db = client["projeto_banco_de_dados"]

colecao_jogos = db["jogos"]

try:
    client.admin.command("ping")
    print("Conectado ao MongoDB!")
except Exception as e:
    print(f"Erro ao conectar: {e}")