from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    TokenSchema,
)
from fast_zero.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['Auth'])

T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]


@router.post('/token', status_code=HTTPStatus.OK, response_model=TokenSchema)
def login_from_access_token(
    form_data: T_OAuth2Form,
    session: T_Session,
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
