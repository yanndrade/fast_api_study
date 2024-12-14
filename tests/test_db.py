from sqlalchemy import select

from fastapizero.models import User


def test_create_user(session):
    user = User(
        username='TestUser',
        password='test_password',
        email='teste@teste.com',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(
        select(User).where(User.email == 'teste@teste.com')
    )

    assert result.username == 'TestUser'
    assert result.id == 1
