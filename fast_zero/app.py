from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    MessageSchema,
    TokenSchema,
    UserListSchema,
    UserPublicSchema,
    UserSchema,
)
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def read_root():
    return {'message': 'Hello World!'}


# users
@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Username {user.username} already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Email {user.email} already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserListSchema)
def read_users(
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
):
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def read_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with id {user_id} not found',
        )

    return db_user


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='You are not authorized to update this user',
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=MessageSchema
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='You are not authorized to update this user',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


# auth
@app.post('/token', status_code=HTTPStatus.OK, response_model=TokenSchema)
def login_from_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    db_user = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with email {form_data.username} not found',
        )

    is_verify_password = verify_password(form_data.password, db_user.password)

    if not is_verify_password:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': db_user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
