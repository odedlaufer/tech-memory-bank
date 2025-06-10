from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import SessionLocal
from fastapi import HTTPException
from typing import List
from ..auth import get_current_user
from ..models import User
from ..utils.summarizer import summarize_text

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/learn", response_model=schemas.NoteOut)
def learn(note: schemas.NoteCreate, db: Session = Depends(get_db),
          user: User = Depends(get_current_user)):
    return crud.create_note(db=db, note=note, user_id=user.id)  # type: ignore


@router.get("/explain/{title}", response_model=schemas.NoteOut)
def explain_note(title: str, db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    note = crud.get_note_by_title(db, title=title)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/search", response_model=List[schemas.NoteOut])
def search_notes(tags: str, db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    return crud.search_notes_by_tags(db, tags=tags)


@router.get("/user-notes", response_model=List[schemas.NoteOut])
def get_user_notes(db: Session = Depends(get_db), 
                   user: User = Depends(get_current_user)):
    return db.query(models.Note).filter(models.Note.owner_id == user.id).all()


@router.put("/update/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int,
                note_update: schemas.NoteUpdate,
                db: Session = Depends(get_db),
                user: User = Depends(get_current_user)):
    
    updated = crud.update_note(db=db,
                               note_id=note_id,  # type: ignore
                               user_id=user.id,  # type: ignore
                               updated_data=note_update)  # type: ignore
    if not updated:
        return HTTPException(status_code=404, detail="Note not found or unauthorized")
    return updated


@router.post("/summarize")
def summarize_note_content(content: str, user: User = Depends(get_current_user)):
    if len(content.split()) < 30:
        raise HTTPException(status_code=400, detail="Content is too short to summarize")
    summary = summarize_text(content)
    return {"summary": summary}