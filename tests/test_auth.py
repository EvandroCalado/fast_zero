from http import HTTPStatus


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
