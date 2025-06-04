from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note_by_title(db: Session, title: str):
    return db.query(models.Note).filter(models.Note.title == title).first()


def search_notes_by_tags(db: Session, tags: str):
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    filters = [models.Note.tags.ilike(f"%{tag}%") for tag in tag_list]
    return db.query(models.Note).filter(or_(*filters)).all()


def update_note(db: Session, note_id: int, user_id: int, updated_data: schemas.NoteUpdate):
    note = db.query(models.Note).filter(models.Note.id == note_id, 
                                        models.Note.owner_id == user_id).first()

    if updated_data.title is not None:
        note.title = updated_data.title  # type: ignore

    if updated_data.content is not None:
        note.content = updated_data.content  # type: ignore

    if updated_data.tags is not None:
        note.tags = updated_data.tags  # type: ignore

    db.commit()
    db.refresh(note)
    return note
