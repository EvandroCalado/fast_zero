from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import settings


def test_security_should_be_create_access_token():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']


def test_security_should_be_raise_error_if_token_is_invalid(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid_token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
