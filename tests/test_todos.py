from http import HTTPStatus

from fast_zero.models import TodoState
from tests.conftest import TodoFactory


def test_create_todo_should_return_CREATED_and_todos(client, token):
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'valid_title',
            'description': 'valid_description',
            'state': 'draft',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'valid_title',
        'description': 'valid_description',
        'state': 'draft',
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_read_todo_should_return_OK_and_list_of_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_read_todo_should_return_OK_by_offset_and_limit(
    session, client, user, token
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_read_todo_should_return_OK_by_search_with_title(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='valid_title')
    )
    session.commit()

    response = client.get(
        '/todos/?search=valid_title',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_read_todo_should_return_OK_by_search_with_description(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description='valid_title')
    )
    session.commit()

    response = client.get(
        '/todos/?search=valid_title',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_read_todo_should_return_OK_by_state(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_read_todo_should_return_OK_by_search_state_and_limit(
    session, client, user, token
):
    expected_todos = 2
    session.bulk_save_objects(
        TodoFactory.create_batch(
            2, user_id=user.id, title='valid_title', state=TodoState.draft
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='another_valid_title',
            state=TodoState.done,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?search=valid_title&state=draft&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos
    assert response.json()['todos'][0]['title'] == 'valid_title'
    assert response.json()['todos'][0]['state'] == 'draft'

    another_expected_todos = 3
    response = client.get(
        '/todos/?search=another_valid_title&state=done&limit=3',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == another_expected_todos
    assert response.json()['todos'][0]['title'] == 'another_valid_title'
    assert response.json()['todos'][0]['state'] == 'done'


def test_delete_todo_should_return_OK_by_id(session, client, user, token):
    todo = TodoFactory.create(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_todo_should_return_NOT_FOUND_if_id_is_invalid(
    session, client, user, token
):
    todo = TodoFactory.create(user_id=user.id)
    session.add(todo)
    session.commit()

    fake_id = 3

    response = client.delete(
        f'/todos/{fake_id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': f'Task with id {fake_id} not found'}


def test_update_todo_should_return_OK_if_id_is_valid(
    session, client, user, token
):
    todo = TodoFactory.create(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'new_title', 'description': 'new_description'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'title': 'new_title',
        'description': 'new_description',
        'state': 'draft',
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_update_todo_should_return_NOT_FOUND_if_id_is_invalid(client, token):
    fake_id = 3

    response = client.patch(
        f'/todos/{fake_id}',
        json={'title': 'new_title', 'description': 'new_description'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': f'Task with id {fake_id} not found'}
