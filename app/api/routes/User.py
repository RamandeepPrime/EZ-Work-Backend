from fastapi import APIRouter


router = APIRouter()

@router.post('/user')
def create_user():
	return 'hello'