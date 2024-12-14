from http import HTTPStatus

from fastapizero.schemas import UserPublic

# Triple A: Arrange, Act, Assert
# Arrange: Set up the request
# Act: Perform the request
# Assert: Check the response


def test_read_root_deve_retornar_ok_e_hello_world(client):
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    # Assert (Verificação)
    assert response.json() == {'message': 'Hello World!'}


# Exercicio Aula2
def test_read_hello_deve_retornar_ok_e_hello_world(client):
    response = client.get('/hello')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    # Assert (Verificação)
    assert '<h1>Hello World!</h1>' in response.text


def test_create_user(client):
    response = client.post(  # Act (Ação)
        # Validar UserSchema
        '/users/',
        json={
            'username': 'TestUser',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    # Validar UserPublic
    # Assert (Verificação)
    # Status Code
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'TestUser',
        'email': 'test@test.com',
    }


def test_create_user_username_deve_retornar_bad_request(client, user):
    response = client.post(  # Act (Ação)
        # Validar UserSchema
        '/users/',
        json={
            'username': 'TestUser',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}
    # Assert (Verificação)


def test_create_user_email_deve_retornar_bad_request(client, user):
    response = client.post(  # Act (Ação)
        # Validar UserSchema
        '/users/',
        json={
            'username': 'UserTest',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}
    # Assert (Verificação)


def test_read_users(client):
    response = client.get('/users/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    assert response.json() == {  # Assert (Verificação)
        'users': []
    }


def test_read_users_with_users(client, user):
    response = client.get('/users/')  # Act (Ação)
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    assert response.json() == {  # Assert (Verificação)
        'users': [user_schema]
    }


def test_read_user_by_id(client, user):
    response = client.get('/users/1')  # Act (Ação)
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    assert response.json() == user_schema  # Assert (Verificação)


def test_read_user_by_id_deve_retornar_not_found(client, user):
    response = client.get('/users/99999999999')  # Act (Ação)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Verificação)
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(  # Act (Ação)
        '/users/1',
        json={
            'username': 'TestModif',
            'password': 'passwordModif',
            'email': 'testmodif@testmodif.com',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    assert response.json() == {
        'username': 'TestModif',
        'email': 'testmodif@testmodif.com',
        'id': 1,
    }


def test_update_user_deve_retorna_not_found(client, user):
    response = client.put(  # Act (Ação)
        '/users/999999999999999999',
        json={
            'username': 'TestModif',
            'password': 'passwordModif',
            'email': 'testmodif@testmodif.com',
            'id': 1,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Verificação)
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')  # Act (Ação)

    # Assert (Verificação)
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_user_deve_retornar_not_found(client, user):
    response = client.delete('/users/999999999')  # Act (Ação)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Verificação)
    assert response.json() == {'detail': 'User not found'}
