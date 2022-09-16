from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

from fastapi import FastAPI
from api.routes.api import router
from database.models import tables
from database.db import engine

tables.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(router, prefix='')
