from typing import Union
from fastapi import APIRouter, Depends, Response
from resources.jwt_verify import oauth2_scheme
from database.schemas import user as schema
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post('/token')
def token(form_data: OAuth2PasswordRequestForm=Depends()):
	return {'access_token': form_data.username}


# @router.get('/auth/sendVerificationLink')
@router.get('/')
def verification_link(token: str = Depends(oauth2_scheme)):
	print(token)
	return {
		"token" : token
	}


#bcript the token the then send it to user with html