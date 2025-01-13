from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapizero.database import get_session
from fastapizero.models import ToDos, User
from fastapizero.schemas import (
    Message,
    ToDoList,
    ToDoPublic,
    ToDoSchema,
    ToDoState,
)
from fastapizero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ToDoPublic)
def create_todo(todo: ToDoSchema, user: T_CurrentUser, session: T_Session):
    db_todo = ToDos(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=ToDoList, status_code=HTTPStatus.OK)
def list_todos(  # noqa
    session: T_Session,
    user: T_CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: ToDoState | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = session.query(ToDos).where(ToDos.user_id == user.id)
    if title:
        query = query.filter(ToDos.title.contains(title))
    if description:
        query = query.filter(ToDos.description.contains(description))
    if state:
        query = query.filter(ToDos.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()
    return {'todos': todos}


@router.delete('/{todo_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_todo(
    todo_id: int,
    user: T_CurrentUser,
    session: T_Session,
):
    todo = session.scalar(
        select(ToDos).where(ToDos.id == todo_id, ToDos.user_id == user.id)
    )
    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Todo not found'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Todo deleted successfully'}
