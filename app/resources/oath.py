
from resources.jwt_verify import oauth2_scheme
from fastapi import Depends
from .jwt_verify import get_user_from_token

def get_user_token(token: str=Depends(oauth2_scheme)):
	return get_user_from_token(token)
