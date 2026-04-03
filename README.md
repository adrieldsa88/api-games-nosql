# 🎮 Sistema de Avaliação de Jogos

API REST para gerenciar usuários, jogos e avaliações com autenticação JWT.

## 🛠️ Tecnologias

- FastAPI
- MongoDB
- PyJWT (Autenticação)
- Passlib + Bcrypt
- Pydantic

## 📦 Instalação

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Configure o arquivo `.env`:
```env
DB_URL=mongodb://localhost:27017
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## ▶️ Executar

```bash
uvicorn main:app --reload
```

API: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

## 📚 Endpoints

- `POST /api/usuarios/` - Registrar
- `POST /api/usuarios/login` - Fazer login
- `POST /api/jogos/` - Criar jogo
- `GET /api/jogos/` - Listar jogos
- `POST /api/avaliacoes/` - Criar avaliação (⚠️ requer autenticação)
- `GET /api/avaliacoes/jogo/{titulo}` - Listar avaliações

## 🔐 Autenticação

Para acessar rotas protegidas, envie o token no header:
```
Authorization: Bearer seu_token_aqui
```

### Jogos
- `POST /api/jogos/` - Criar jogo
- `GET /api/jogos/` - Listar jogos
- `GET /api/jogos/{titulo}` - Detalhes do jogo
- `PATCH /api/jogos/{titulo}` - Atualizar
- `DELETE /api/jogos/{titulo}` - Deletar

### Avaliações
- `POST /api/avaliacoes/` - Criar avaliação
- `GET /api/avaliacoes/jogo/{titulo}` - Reviews do jogo
- `GET /api/avaliacoes/usuario/{email}` - Reviews do usuário
- `DELETE /api/avaliacoes/{id_avaliacao}` - Deletar avaliação

## Exemplo de Uso 💡

```bash
# 1. Criar usuário
curl -X POST http://localhost:8000/api/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"João","email":"joao@ex.com"}'

# 2. Criar jogo
curl -X POST http://localhost:8000/api/jogos/ \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Elden Ring","genero":"RPG"}'

# 3. Avaliar jogo
curl -X POST http://localhost:8000/api/avaliacoes/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo_jogo":"Elden Ring",
    "email_usuario":"joao@ex.com",
    "nota":9.5,
    "review":"Excelente!"
  }'
```

## Popular Banco 📊

```bash
python populate_db.py
```

Cria 5 usuários, 7 jogos e 12 avaliações 

## Validações ✅

- Nota: 0-10
- Email: Deve ser único por usuário
- Titulo: Sem duplicatas




