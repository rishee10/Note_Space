from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt
from auth import SECRET_KEY, ALGORITHM
from database import get_db
from sqlalchemy.orm import Session
from models import Note

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data["user_id"]
    except:
        return None

@router.get("/notes")
def notes_page(request: Request, db: Session = Depends(get_db)):
    user_id = get_user(request)
    if not user_id:
        return RedirectResponse("/login")
    notes = db.query(Note).filter(Note.owner_id == user_id).all()
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})

@router.post("/add-note")
def add_note(request: Request, topic: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    user_id = get_user(request)
    note = Note(topic=topic, description=description, owner_id=user_id)
    db.add(note)
    db.commit()
    return RedirectResponse("/notes", status_code=302)

@router.get("/edit/{note_id}")
def edit_page(note_id: int, request: Request, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    return templates.TemplateResponse("edit_note.html", {"request": request, "note": note})

@router.post("/edit/{note_id}")
def edit_note(note_id: int, topic: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    note.topic = topic
    note.description = description
    db.commit()
    return RedirectResponse("/notes", status_code=302)

@router.get("/delete/{note_id}")
def delete(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    db.delete(note)
    db.commit()
    return RedirectResponse("/notes", status_code=302)
