# Sistema de Avaliação de Jogos 🎮

API simples e rápida para gerenciar e avaliar jogos com MongoDB.

## Características ✨

- **Gerenciamento de Usuários**: Criar e listar usuários
- **Gerenciamento de Jogos**: CRUD completo sem complicações
- **Sistema de Avaliações**: Usuários podem avaliar jogos simplemente
- **Cálculo Automático de Média**: Média de avaliações atualizada em tempo real

## Tecnologias Utilizadas 🛠️

- **FastAPI**: Framework web
- **MongoDB**: Banco de dados NoSQL
- **Python 3.x**

## Instalação 📦

### 1. Ambiente virtual
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar .env
```env
DB_URL=mongodb://localhost:27017
```

## Como Executar 🚀

```bash
uvicorn main:app --reload
```

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

## Endpoints Principais 🔌

### Usuários
- `POST /api/usuarios/` - Criar usuário
- `GET /api/usuarios/` - Listar usuários
- `GET /api/usuarios/{email}` - Detalhes do usuário

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




