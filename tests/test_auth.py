from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_get_token_username_error(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': 'ErrorUser',
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'access_token' not in token


def test_get_token_password_error(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.username,
            'password': 'ErrorPassword',
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'access_token' not in token
