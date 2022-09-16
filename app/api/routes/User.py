from typing import Union
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from resources.jwt_verify import create_jwt_token
from database.schemas import user as schema
from database.dependencies import get_session
from database.models.queries import user as queries

from database.schemas.responses import SuccessResponse, ErrorResponse
from database.schemas.error import EntityNotFound, EntityAlreadyExists


router = APIRouter()


@router.post('/signup', response_model=Union[SuccessResponse, ErrorResponse])
def signup(user: schema.CreateUser, response: Response, db: Session = Depends(get_session)):
    try:
        queries.create_user(db, user)

    except EntityAlreadyExists as e:

        response.status_code = 400
        return ErrorResponse(erors=[str(e)])

    return SuccessResponse(message="User has been succesfully created")


@router.post('/login', response_model=Union[ErrorResponse, schema.UserToken])
def login(user: schema.UserInLogIn, response: Response, db: Session = Depends(get_session)):

    try:

        curr_user = queries.verify_user(db, user)

    except EntityNotFound as e:

        response.status_code = 400
        return ErrorResponse(
            errors=[str(e)]
        )

    token = create_jwt_token(schema.User(username = curr_user.username, email = curr_user.email,
                                         userType = curr_user.userType))

    return schema.UserToken(
        token = token
    )
