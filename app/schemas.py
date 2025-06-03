from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[str] = ""


class NoteOut(NoteCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
