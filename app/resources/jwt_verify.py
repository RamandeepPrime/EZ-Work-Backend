from datetime import timedelta, datetime
import os
from jose import jwt
from database.schemas import user as schema
from pydantic import ValidationError
from database.schemas.error import JwtError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(plain_text_password):
	return pwd_context.hash(plain_text_password)


def verify_password(plain_text_password, hashed_password):	
	return pwd_context.verify(plain_text_password, hashed_password)


def create_jwt_token(user: schema.User,expires_delta: timedelta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)): 

	to_encode=user.dict().copy()
	expire = datetime.utcnow() + expires_delta
	to_encode.update({
		'exp': expire
	})
	return jwt.encode(to_encode, JWT_SECRET, algorithm = JWT_ALGORITHM)


def get_user_from_token(token: str):

	try:
		return schema.User(**jwt.decode(token, JWT_SECRET, algorithms= [JWT_ALGORITHM]))

	except jwt.PyJWTError as decode_error:
		raise JwtError("Unable to decode JWT token")
	
	except ValidationError as validation_error:
		raise JwtError("Payload is changed in token")




