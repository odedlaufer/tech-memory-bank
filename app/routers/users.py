from fastapi import APIRouter, Depends
from .. import schemas, auth, models
from ..database import SessionLocal


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/me", response_model=schemas.UserOut)
def get_me(user: models.User = Depends(auth.get_current_user)):
    return user
