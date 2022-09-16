from fastapi import APIRouter
from api.routes import User,authentication


router = APIRouter()

router.include_router(User.router, tags=['user'],prefix='')
router.include_router(authentication.router, tags=['authentication'],prefix='')

