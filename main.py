from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router_usuarios, router_jogos, router_avaliacoes

app = FastAPI(
    title="Sistema de Avaliação de Jogos",
    description="API simples para avaliar jogos",
    version="2.0.0"
)

app.include_router(router_usuarios)
app.include_router(router_jogos)
app.include_router(router_avaliacoes)