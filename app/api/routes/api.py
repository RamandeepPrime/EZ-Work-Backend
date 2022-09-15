from fastapi import APIRouter
from api.routes import User

router = APIRouter()

router.include_router(User.router, tags=['user'],prefix='')
