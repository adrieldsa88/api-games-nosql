from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Gerenciador de Jogos NoSQL",
    description="API feita com FastAPI para gerenciar jogos no MongoDB",
    version="1.0.1"
)

app.include_router(router)