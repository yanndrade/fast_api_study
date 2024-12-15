from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapizero.database import get_session
from fastapizero.models import User
from fastapizero.schemas import (
    Message,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapizero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
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
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
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
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Not enough permissions',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)
    return current_user


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Not enough permissions',
        )

    session.delete(current_user)
    session.commit()
    return {'message': 'User deleted successfully'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user_db = session.scalar(
        select(User).where(User.username == form_data.username)
    )
    if not user_db or not verify_password(
        form_data.password, user_db.password
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        )
    access_token = create_access_token(data_payload={'sub': user_db.username})
    return {'access_token': access_token, 'token_type': 'Bearer'}
