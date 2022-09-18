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
from fastapi.responses import JSONResponse

import os

PASSKEY = Fernet.generate_key()
fernet = Fernet(PASSKEY)


router = APIRouter()


@router.post('/signup', response_model=Union[SuccessResponse, ErrorResponse])
def signup(user: schema.CreateUser, response: Response, db: Session = Depends(get_session)):
    
    try:
        curr_user=queries.create_user(db, user)

    except EntityAlreadyExists :

        return JSONResponse(status_code=400, content={'message': 'user_already_exists'})
    
    token = create_jwt_token(schema.User(username = curr_user.username, email = curr_user.email,
                                         userType = curr_user.userType))
    # return SuccessResponse(message="User has been succesfully created")
    return JSONResponse(status_code=200, content={'message': 'User has been succesfully created',
                                                                    'token':f"{token}"})



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
def disable_user(response: Response, curr_user: schema.DisableUser, user: schema.User = Depends(get_user_token), db: Session = Depends(get_session)):
    
    
    if(user.userType=='Client'):
        response.status_code = 401
        return ErrorResponse(
            errors=["You are not authorized to do this operation"]
        )
    
    banned_user = queries.get_user(db, curr_user.email)
    
    if(not banned_user):
        response.status_code = 400
        return  ErrorResponse(
            errors=[f'''User with email: {curr_user.email} does not exist''']
        )
    if(banned_user.isDisabled):

        if(curr_user.action):
            response.status_code = 400
            return  ErrorResponse(
                errors=[f'''User with email: {banned_user.email}  already disabled''']
            )
        else:#enabling the user
            banned_user.isDisabled=0
            db.add(banned_user)
            db.commit()
            return SuccessResponse(message=f'''User with email: {banned_user.email} has been enabled ''')


    banned_user.isDisabled=1
    db.add(banned_user)
    db.commit()
    return SuccessResponse(message=f'''User with email: {banned_user.email} has been disabled''')


@router.get('/logout', response_model=Union[ErrorResponse, SuccessResponse])
def logout(response: Response, token: schema.UserToken = Depends(oauth2_scheme)):
    
    pattern=f'token:{token}'
    if(get_token_redis(pattern)):
        delete_token_redis(pattern)
    
        return SuccessResponse(message='Succesfully logged out')
    
    response.status_code = 400
    return ErrorResponse(
        errors=['Already logged out']
    )
    