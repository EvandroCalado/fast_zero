from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserDB)
def create_user(user: UserSchema):
    use_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(use_with_id)

    return use_with_id


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def read_user_by_id(user_id: int):
    return database[user_id - 1]


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with id {user_id} not found',
        )

    user_with_id = UserDB(id=user_id, **user.model_dump())

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'User with id {user_id} not found',
        )

    database.pop(user_id - 1)

    return {'message': 'User deleted'}
