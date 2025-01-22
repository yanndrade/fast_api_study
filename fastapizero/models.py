from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class ToDoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class ToDos:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[ToDoState]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Exercício 1 - Adicione os campos created_at e updated_at
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
