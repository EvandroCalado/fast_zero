from http import HTTPStatus

from fast_zero.schemas import UserPublicSchema


def test_users_read_root_should_return_OK_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_users_create_user_should_return_CREATED_and_user_with_id(client):
    response = client.post(
        '/users/',
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
    }


def test_users_create_user_should_return_BAD_REQUEST_if_username_exists(
    client, user
):
    response = client.post(
        '/users/',
        json={
            'username': 'test_user',
            'email': 'test_user@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_users_create_user_should_return_BAD_REQUEST_if_email_exists(
    client, user
):
    response = client.post(
        '/users/',
        json={
            'username': 'new_test_user',
            'email': 'test_user@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_users_read_users_should_return_OK_and_empty_list(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_users_read_users_should_return_OK_and_users_list(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_users_read_user_should_return_OK_and_user(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test_user',
        'email': 'test_user@me.com',
    }


def test_users_read_user_should_return_NOT_FOUND_if_id_is_invalid(
    client, user
):
    response = client.get('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_users_update_user_should_return_OK_and_updated_user(client, user):
    response = client.put(
        '/users/1',
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
    }


def test_users_update_user_should_return_NOT_FOUND_if_id_is_invalid(
    client, user
):
    response = client.put(
        '/users/3',
        json={
            'username': 'updated_johndoe',
            'email': 'johndoe@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_users_update_user_should_return_CONFLICT_if_id_already_exists(
    client, user
):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'test_user@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_users_update_user_should_return_CONFLICT_if_email_already_exists(
    client, user
):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'test',
            'email': 'fausto@example.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_users_delete_user_should_return_OK_and_user_deleted(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_users_delete_user_should_return_NOT_FOUND_if_id_is_invalid(
    client, user
):
    response = client.delete('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND
