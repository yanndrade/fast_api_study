from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapizero.database import get_session
from fastapizero.models import User
from fastapizero.schemas import (
    Token,
)
from fastapizero.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Oauth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session,
    form_data: T_Oauth2Form,
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


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: T_CurrentUser,
):
    new_access_token = create_access_token(data_payload={'sub': user.username})
    return {'access_token': new_access_token, 'token_type': 'Bearer'}
