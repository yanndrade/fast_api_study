from http import HTTPStatus

from fastapizero.schemas import ToDoState
from tests.conftest import ToDoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        json={
            'title': 'Test Todo',
            'description': 'This is a test todo',
            'state': 'todo',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'state': 'todo',
    }


def test_list_todos_should_return_5_todos(client, token, session, user):
    expected_todos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(expected_todos, user_id=user.id)
    )

    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_with_offset_and_limit(client, token, session, user):
    expected_todos = 2
    session.bulk_save_objects(ToDoFactory.create_batch(5, user_id=user.id))

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_with_title_filter(client, token, session, user):
    expected_todos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, title='test')
    )

    response = client.get(
        '/todos/?title=test', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_with_desc_filter(client, token, session, user):
    expected_todos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(5, user_id=user.id, description='test')
    )

    response = client.get(
        '/todos/?description=test',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_with_state_filter(client, token, session, user):
    expected_todos = 20
    session.bulk_save_objects(
        ToDoFactory.create_batch(20, user_id=user.id, state='todo')
    )

    state = 'todo'

    response = client.get(
        f'/todos/?state={state}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_combined_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        ToDoFactory.create_batch(
            5,
            user_id=user.id,
            title='Test todo combined',
            description='combined description',
            state=ToDoState.done,
        )
    )

    session.bulk_save_objects(
        ToDoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='other description',
            state=ToDoState.todo,
        )
    )
    session.commit()

    response = client.get(
        '/todos/?title=Test todo combined&description=combined&state=done',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(client, token, session, user):
    todo = ToDoFactory.create(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Todo deleted successfully'}


def test_delete_todo_should_return_not_found(client, token, user, session):
    todo = ToDoFactory.create(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f'/todos/{todo.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_todo_state(client, token, user, session):
    todo = ToDoFactory.create(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id}',
        json={'state': 'done'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'state': 'done',
    }


def test_update_todo_title(client, token, user, session):
    todo = ToDoFactory.create(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'Updated title'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': todo.id,
        'title': 'Updated title',
        'description': todo.description,
        'state': todo.state,
    }


def test_todo_update_description(client, token, user, session):
    todo = ToDoFactory.create(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id}',
        json={'description': 'Updated description'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': todo.id,
        'title': todo.title,
        'description': 'Updated description',
        'state': todo.state,
    }


def test_update_todo_should_return_not_found(client, token, user, session):
    todo = ToDoFactory.create(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id + 1}',
        json={'description': 'Updated description'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}
