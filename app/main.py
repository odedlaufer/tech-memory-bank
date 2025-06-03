from fastapi import FastAPI
from . import models
from .database import engine
from .routers import notes, auth as auth_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tech Memory Bank")

app.include_router(notes.router)
app.include_router(auth_router.router)