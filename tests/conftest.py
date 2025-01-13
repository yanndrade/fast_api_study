from contextlib import contextmanager
from datetime import datetime

import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapizero.app import app
from fastapizero.database import get_session
from fastapizero.models import ToDos, ToDoState, User, table_registry
from fastapizero.security import (
    get_password_hash,
)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')


class ToDoFactory(factory.Factory):
    class Meta:
        model = ToDos

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(ToDoState)
    user_id = 1


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def client(session):  # Arrange
    def get_test_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_test_session
        yield client
    app.dependency_overrides.clear()
    # return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    user = UserFactory(password=get_password_hash('test_password'))
    # user = User(
    #    username='TestUser',
    #    password=get_password_hash('test_password'),
    #    email='test@test.com',
    # )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'test_password'

    return user


@pytest.fixture
def other_user(session):
    user = UserFactory()
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token/',
        data={'username': user.username, 'password': user.clean_password},
    )
    return response.json()['access_token']
