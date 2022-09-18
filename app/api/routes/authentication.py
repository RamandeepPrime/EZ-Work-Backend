from typing import Union
from fastapi import APIRouter, Depends, Response
from resources.email_verify import send_verification_link
from database.models.queries.user import get_user
from database.schemas import user as schema
from resources.oath import get_user_token
from sqlalchemy.orm import Session
from resources.jwt_verify import oauth2_scheme, get_user_from_token
from database.dependencies import get_session
from database.schemas.responses import SuccessResponse, ErrorResponse

import os
from .User import fernet,PASSKEY

router = APIRouter()



# @router.post('/token')
# def token(form_data: OAuth2PasswordRequestForm=Depends()):
# 	return {'access_token': form_data.username}


# @router.get('/auth/sendVerificationLink')
# @router.get('/')
# def verification_link(token: str = Depends(oauth2_scheme)):
# 	print(token)
# 	return {
# 		"token" : token
# 	}

@router.get('/auth/sendVerificationLink', response_model=Union[SuccessResponse, ErrorResponse])
def verification_link(response: Response, token: schema.UserToken = Depends(oauth2_scheme), user: schema.User = Depends(get_user_token), db: Session = Depends(get_session)):
	
	
	curr_user=get_user(db, user.email)
	
	if(curr_user.emailVerfied):
		response.status_code=400
		return ErrorResponse(
			errors=['Email already verified!!']
		)

	# REDIS.set(curr_user.email, token, ex = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) * 30) # 30 minutes 1*30
	# bycrpt token
	hashed_token=fernet.encrypt(token.encode()).decode()
	print(hashed_token)
	send_verification_link(curr_user.email, hashed_token)
	# send user email
	return SuccessResponse(message="Verification link has been sent to your registered email account")

	


@router.get('/auth/verify', response_model=Union[SuccessResponse, ErrorResponse])
def verify_email_link(hashed_token:	str, user_email: str, response: Response , db: Session = Depends(get_session)):

	print(hashed_token, user_email)
	token=fernet.decrypt(hashed_token.encode()).decode()

	try:
		
		curr_user=get_user_from_token(token)#get from schemas.user

		if(curr_user.email == user_email):

			database_user=get_user(db, curr_user.email)
			database_user.emailVerfied=1
			db.add(database_user)
			db.commit()
			return SuccessResponse(message="Your email has been verified!!")

		response.status_code = 400
		return ErrorResponse(
			errors=["Wrong email address or token"]
			)

	except Exception as e:
		response.status_code = 400
		return ErrorResponse(
			errors=[str(e)]
			)

	








#bcript the token the then send it to user with html