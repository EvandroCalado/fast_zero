from http import HTTPStatus

from tests.conftest import UserFactory


def test_create_user_should_return_CREATED_and_user_with_id(client):
    response = client.post(
        '/users',
        json={
            'username': 'johndoe',
            'email': 'johndoe@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'johndoe',
        'email': 'johndoe@me.com',
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_create_user_should_return_BAD_REQUEST_if_username_exists(
    client, user
):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'test_user@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_should_return_BAD_REQUEST_if_email_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'new_test_user',
            'email': user.email,
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users_should_return_OK_and_empty_list(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_should_return_OK_and_users_list(client, session):
    expected_users = 5
    session.bulk_save_objects(UserFactory.create_batch(5))
    session.commit()

    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['users']) == expected_users


def test_read_user_should_return_OK_and_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': user.username,
        'email': user.email,
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_read_user_should_return_NOT_FOUND_if_id_is_invalid(client):
    response = client.get('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_should_return_OK_and_updated_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'updated_johndoe',
            'email': 'johndoe@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'updated_johndoe',
        'email': 'johndoe@me.com',
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_update_user_should_return_FORBIDDEN_if_id_is_invalid(
    client, other_user, token
):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'updated_johndoe',
            'email': 'johndoe@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_should_return_CONFLICT_if_username_already_exists(
    client, user, other_user, token
):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': 'test_user@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_update_user_should_return_CONFLICT_if_email_already_exists(
    client, user, other_user, token
):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'new_user_name',
            'email': other_user.email,
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user_should_return_OK_and_user_deleted(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_should_return_FORBIDDEN_if_id_is_invalid(
    client, other_user, token
):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
