from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    FilterTodoSchema,
    MessageSchema,
    TodoListSchema,
    TodoPublicSchema,
    TodoSchema,
    TodoUpdateSchema,
)
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['Todos'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_Filter = Annotated[FilterTodoSchema, Query()]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=TodoPublicSchema
)
def create_todo(
    todo: TodoSchema, session: T_Session, current_user: T_CurrentUser
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=current_user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoListSchema)
def read_todos(
    session: T_Session,
    current_user: T_CurrentUser,
    todo_filter: T_Filter,
):
    query = select(Todo).where(Todo.user_id == current_user.id)

    if todo_filter.search:
        query = query.filter(
            or_(
                Todo.title.ilike(f'%{todo_filter.search}%'),
                Todo.description.ilike(f'%{todo_filter.search}%'),
            )
        )

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    db_todos = session.scalars(
        query.offset(todo_filter.offset).limit(todo_filter.limit)
    ).all()

    return {'todos': db_todos}


@router.delete('/{todo_id}', response_model=MessageSchema)
def delete_todo(todo_id: int, session: T_Session, current_user: T_CurrentUser):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == current_user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Task with id {todo_id} not found',
        )

    session.delete(db_todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{todo_id}', response_model=TodoPublicSchema)
def update_todo(
    todo_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
    todo: TodoUpdateSchema,
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == current_user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Task with id {todo_id} not found',
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
