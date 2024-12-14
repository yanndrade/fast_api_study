from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapizero.database import get_session
from fastapizero.models import User
from fastapizero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()


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


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
    db_user = User(
        username=user.username, password=user.password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_to_update = session.scalar(select(User).where(User.id == user_id))
    if not user_to_update:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_to_update.username = user.username
    user_to_update.email = user.email
    user_to_update.password = user.password
    session.commit()
    session.refresh(user_to_update)
    return user_to_update


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_to_delete = session.scalar(select(User).where(User.id == user_id))
    if not user_to_delete:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    session.delete(user_to_delete)
    session.commit()
    return {'message': 'User deleted successfully'}
