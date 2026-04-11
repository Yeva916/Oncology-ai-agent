from app.db.postgres_db import models

from fastapi import FastAPI
from app.db.postgres_db.session import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router
@app.get("/")
def read_root():
    return {"Hello": "World"}