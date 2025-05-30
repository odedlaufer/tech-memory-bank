from fastapi import FastAPI
from . import models
from .database import engine
from .routers import notes


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tech Memory Bank")

app.include_router(notes.router)