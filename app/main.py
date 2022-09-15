from fastapi import FastAPI
from api.routes.api import router



app = FastAPI()


app.include_router(router, prefix='')
