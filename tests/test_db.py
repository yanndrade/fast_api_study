from dataclasses import asdict

from fastapizero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(
            username='TestUser', password='test_password', email='test@test'
        )
        session.add(user)
        session.commit()
    assert asdict(user) == {
        'id': 1,
        'username': 'TestUser',
        'password': 'test_password',
        'email': 'test@test',
        'created_at': time,
        'updated_at': time,
    }
