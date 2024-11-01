from http import HTTPStatus

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


def test_read_users(client):
    response = client.get('/users/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    assert response.json() == {  # Assert (Verificação)
        'users': [{'id': 1, 'username': 'TestUser', 'email': 'test@test.com'}]
    }


def test_update_user(client):
    response = client.put(  # Act (Ação)
        '/users/1',
        json={
            'username': 'TestModif',
            'password': 'passwordModif',
            'email': 'testmodif@testmodif.com',
            'id': 1,
        },
    )

    # assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    assert response.json() == {  # Assert (Verificação)
        'id': 1,
        'username': 'TestModif',
        'email': 'testmodif@testmodif.com',
    }


def test_delete_user(client):
    response = client.delete('/users/1')  # Act (Ação)

    # Assert (Verificação)
    assert response.json() == {'message': 'User deleted'}
