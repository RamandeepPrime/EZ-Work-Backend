from distutils.log import error
from typing import Union
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from resources.jwt_verify import create_jwt_token, oauth2_scheme, get_token_redis, delete_token_redis, set_token_redis
from database.schemas import user as schema
from database.dependencies import get_session
from database.models.queries import user as queries
from resources.oath import get_user_token

from database.schemas.responses import SuccessResponse, ErrorResponse
from database.schemas.error import EntityNotFound, EntityAlreadyExists, DisabledError
from cryptography.fernet import Fernet

import os

PASSKEY = Fernet.generate_key()
fernet = Fernet(PASSKEY)


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

    except (EntityNotFound, DisabledError) as e:

        response.status_code = 400
        return ErrorResponse(
            errors=[str(e)]
        )

    token = create_jwt_token(schema.User(username = curr_user.username, email = curr_user.email,
                                         userType = curr_user.userType))
    
    set_token_redis(f'''token:{token}''', curr_user.email ,int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))*60)

    return schema.UserToken(
        token = token
    )


@router.get('/disableUser', response_model=Union[SuccessResponse, ErrorResponse])
def disable_user(response: Response, user_email: schema.UserEmail, action:bool, user: schema.User = Depends(get_user_token), db: Session = Depends(get_session)):
    
    print(user.email, user.userType)
    if(user.userType=='Client'):
        response.status_code = 400
        return ErrorResponse(
            errors=["You are not authorized to do this operation or refresh the token"]
        )
    
    banned_user = queries.get_user(db, user_email.email)
    
    if(not banned_user):
        response.status_code = 400
        return  ErrorResponse(
            errors=[f'''User with email: {user_email.email} does not exist''']
        )
    if(banned_user.isDisabled):

        if(action):
            response.status_code = 400
            return  ErrorResponse(
                errors=[f'''User with email: {banned_user.email}  already disabled''']
            )
        else:#enabling the user
            banned_user.isDisabled=0
            db.add(banned_user)
            db.commit()
            return SuccessResponse(message=f'''User with email: {banned_user.email} has been enbled ''')


    banned_user.isDisabled=1
    db.add(banned_user)
    db.commit()
    return SuccessResponse(message=f'''User with email: {banned_user.email} has been disabled''')


@router.get('/logout', response_model=Union[ErrorResponse, SuccessResponse])
def logout(response: Response, token: schema.UserToken = Depends(oauth2_scheme)):
    
    pattern=f'token:{token}'
    if(get_token_redis(pattern)):
        delete_token_redis(pattern)
    
        return SuccessResponse(message='Succesfully loged out')
    
    response.status_code = 400
    return ErrorResponse(
        errors=['Already logged out']
    )
    