from pydantic import BaseModel, ConfigDict, EmailStr

from fastapizero.models import ToDoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class ToDoSchema(BaseModel):
    title: str
    description: str
    state: ToDoState


class ToDoPublic(ToDoSchema):
    id: int


class ToDoList(BaseModel):
    todos: list[ToDoPublic]


class ToDoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: ToDoState | None = None
