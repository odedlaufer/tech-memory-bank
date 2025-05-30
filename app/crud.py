from sqlalchemy.orm import Session
from . import models, schemas


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = models.Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note_by_title(db: Session, title: str):
    return db.query(models.Note).filter(models.Note.title == title).first()


def search_notes_by_tag(db: Session, tag: str):
    return db.query(
        models.Note).filter(
        models.Note.tags.ilike(f"%{tag}%")).all()
