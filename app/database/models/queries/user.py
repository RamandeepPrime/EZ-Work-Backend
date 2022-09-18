
from ..tables import User

from sqlalchemy.orm import Session

# schemas
from database.schemas.user import CreateUser,UserInLogIn
from database.schemas.error import EntityAlreadyExists,EntityNotFound, DisabledError

# jwt verification
from resources.jwt_verify import get_hashed_password,verify_password




def get_user(db: Session, email: str):
	return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: CreateUser):
	
	try:

		if(get_user(db,user.email) is not None):
			raise EntityAlreadyExists('User Already Exists.')

	except EntityNotFound:
		pass
	
	new_user=User(username=user.username,email=user.email,password=get_hashed_password(user.password))
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user


def verify_user(db: Session, user: UserInLogIn):
	
	login_user=get_user(db, user.email)

	if(login_user is None or not verify_password(user.password, login_user.password)):
		raise EntityNotFound('Invalid Credentials')
	
	if(login_user.isDisabled):
		raise DisabledError("You can't login because you are banned by Operation User")

	return login_user

	

	

