from pydantic import BaseModel, EmailStr
from typing import Optional
from resources.userTypes import UserTypes


class User(BaseModel):
	username: str
	email: EmailStr
	userType: Optional[UserTypes]=UserTypes.Client


class UserInLogIn(BaseModel):
	email: EmailStr
	password: str

class CreateUser(UserInLogIn):
	username: str

class UserToken(BaseModel):
	token: str

class UserEmail(BaseModel):
	email: EmailStr

class DisableUser(BaseModel):
	email: EmailStr
	action: bool