from http import HTTPStatus

from freezegun import freeze_time


def test_login_should_return_OK_and_token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_login_should_return_NOT_FOUND_if_username_not_found(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'invalid_user',
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_login_should_return_UNAUTHORIZED_if_password_not_valid(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': 'invalid_password',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_should_return_UNAUTHORIZED_if_token_expires(client, user):
    with freeze_time('2023-10-15 12:00:00'):
        response = client.post(
            '/auth/token',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-10-15 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'new_valid_user',
                'email': 'new_valid_email',
                'password': user.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_should_refreah_token_if_token_is_valid(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_token_should_not_refreah_token_if_time_is_expired(client, user):
    with freeze_time('2023-10-15 12:00:00'):
        response = client.post(
            '/auth/token',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-10-15 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
