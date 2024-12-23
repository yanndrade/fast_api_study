from http import HTTPStatus

from freezegun import freeze_time


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


def test_token_expired_after_time(client, user):
    with freeze_time('2024-01-01 00:00:00'):
        response = client.post(
            'auth/token',
            data={
                'username': user.username,
                'password': user.clean_password,
            },
        )

        token = response.json()['access_token']

        assert response.status_code == HTTPStatus.OK
        assert 'access_token' in response.json()
        assert response.json()['token_type'] == 'Bearer'

    with freeze_time('2024-01-01 00:31:00'):
        response = client.delete(
            f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_expired_after_time2(client, user):
    with freeze_time('2024-01-01 00:00:00'):
        response = client.post(
            'auth/token',
            data={
                'username': user.username,
                'password': user.clean_password,
            },
        )

        token = response.json()['access_token']

        assert response.status_code == HTTPStatus.OK
        assert 'access_token' in response.json()
        assert response.json()['token_type'] == 'Bearer'

    with freeze_time('2024-01-01 00:29:00'):
        response = client.delete(
            f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'User deleted successfully'}


def test_refresh_token(client, token):
    response = client.post(
        'auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'Bearer'
