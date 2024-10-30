from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapizero.app import app

# Triple A: Arrange, Act, Assert
# Arrange: Set up the request
# Act: Perform the request
# Assert: Check the response


def test_read_root_deve_retornar_ok_e_hello_world():
    client = TestClient(app)  # Arrange (Organização)

    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    # Assert (Verificação)
    assert response.json() == {'message': 'Hello World!'}

#Exercicio Aula2
def test_read_hello_deve_retornar_ok_e_hello_world():
    client = TestClient(app)  # Arrange (Organização)

    response = client.get('/hello')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Verificação)
    # Assert (Verificação)
    assert '<h1>Hello World!</h1>' in response.text
