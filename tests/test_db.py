from sqlalchemy import select

from fast_zero.models import User


def test_db_should_create_user(session):
    user = User(
        username='johndoe', email='johndoe@me.com', password='password'
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'johndoe@me.com'))

    assert result.username == 'johndoe'
    assert result.email == 'johndoe@me.com'
    assert result.password == 'password'
