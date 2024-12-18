from http import HTTPStatus

from jwt import decode

from fastapizero.security import (
    create_access_token,
)
from fastapizero.settings import Settings


def test_jwt():
    data = {'sub': 'testUser'}
    token = create_access_token(data_payload=data)

    result = decode(
        token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp'] is not None


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer InvalidToken'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_user_not_found(client):
    token = create_access_token(data_payload={'sub': 'testUser'})
    result = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    assert result.status_code == HTTPStatus.UNAUTHORIZED
    assert result.json() == {'detail': 'Could not validate credentials'}


def test_jwt_not_username(client):
    token = create_access_token(data_payload={'name': 'testUser'})
    result = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    assert result.status_code == HTTPStatus.UNAUTHORIZED
    assert result.json() == {'detail': 'Could not validate credentials'}
