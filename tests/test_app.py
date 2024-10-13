from http import HTTPStatus


def test_read_root_should_return_OK_and_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_create_user_should_return_CREATED_and_user_with_id(client):
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


def test_read_users_should_return_OK_and_users_list(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'johndoe', 'email': 'johndoe@me.com'},
        ]
    }


def test_read_user_should_return_OK_and_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'johndoe',
        'email': 'johndoe@me.com',
    }


def test_update_user_should_return_OK_and_updated_user(client):
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


def test_update_user_should_return_NOT_FOUND_if_id_is_invalid(client):
    response = client.put(
        '/users/3',
        json={
            'username': 'updated_johndoe',
            'email': 'johndoe@me.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user_should_return_OK_and_user_deleted(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_should_return_NOT_FOUND_if_id_is_invalid(client):
    response = client.delete('/users/3')

    assert response.status_code == HTTPStatus.NOT_FOUND
