# API Projeto Banco de Dados II

## Objetivo e Escolha

### Objetivo
Implementar uma API que realiza operações CRUD em um banco de dados não relacional 
que gerencie uma coleção de jogos e permita fazer buscas e alterações

### Justificativa
Foi escolhido essa estrutura e lingaguem pela praticidade e também por serem tecnologias muito utilizadas no mercado de trabalho.

## Funcionalidades
- **CRUD Completo**: Inserção (Create), Listagem (Read), Atualização (Update) e Deleção (Delete).
- **Filtros Dinâmicos**: Busca por título, gênero e filtros de nota mínima ou ano.
- **Atualização Inteligente**: O endpoint de atualização altera apenas os campos enviados no JSON
- **Validação Automática**: Garante que anos sejam inteiros e notas sejam números decimais.

## Estrutura do Banco de Dados e Tecnologias Utilizadas

### Tipo de Banco de Dados Utilizado

O projeto utiliza **MongoDB**, que é um banco de dados **NoSQL orientado a documentos**.

Nesse tipo de banco, os dados são armazenados em **documentos no formato JSON ou BSON**, organizados dentro de **coleções**. 
No projeto foi utilizada a coleção **`jogos`**, responsável por armazenar as informações de cada jogo cadastrado no sistema.

### Estrutura dos Dados

Cada jogo é armazenado como um **documento JSON** dentro da coleção `jogos`.

#### Exemplo de documento
Foi escolhido JSON pela praticidade e por ser a mais difundida

```json
{
  "titulo": "The Witcher 3",
  "genero": "RPG",
  "ano": 2015,
  "nota": 9.8
}
```

## Linguagem Utilizada
 Foi escolhida a linguagem Python, fazendo uso do framework FastAPI e das bibliotecas:
 - pymongo(para conectar-se ao banco MongoDB)
 - uvicorn(servidor para rodar a API)
 - pydantic(para tipagem de dados)

 ## Como rodar a API
 - Criar um ambiente virtual(mais recomendado)
 - Instalar as bibliotecas utilizadas
```
pip install requirements.txt
```
 - Criar o banco de dados MongoDB
 - Executar o comando 
```
uvicorn main:app --reload
```
 - Acessar a documentação no localhost/docs


