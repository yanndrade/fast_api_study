from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapizero.routers import auth, todos, users
from fastapizero.schemas import (
    Message,
)

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


# Create (Criar): adicionar novos registros ao banco de dados.
# Read (Ler): recuperar registros existentes do banco de dados.
# Update (Atualizar): modificar registros existentes no banco de dados.
# Delete (Excluir): remover registros existentes do banco de dados.


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Hello World!'}


# Exercicio Aula2
@app.get('/hello', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_hello():
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1>Hello World!</h1>
      </body>
    </html>"""
