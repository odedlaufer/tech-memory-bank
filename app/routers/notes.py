from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal
from fastapi import HTTPException

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/learn", response_model=schemas.NoteOut)
def learn(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db=db, note=note)


@router.get("/explain/{title}", response_model=schemas.NoteOut)
def explain_note(title: str, db: Session = Depends(get_db)):
    note = crud.get_note_by_title(db, title=title)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
