from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from models import Note, User
from auth import decode_token
from typing import Optional

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except Exception:
        return None

@router.get("/notes")
def notes_page(request: Request, tag: Optional[str] = None, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    if tag:
        # filter notes where tags contain the provided tag (simple substring match)
        notes = db.query(Note).filter(Note.owner_id == user.id, Note.tags.like(f"%{tag}%")).order_by(Note.id.desc()).all()
    else:
        notes = db.query(Note).filter(Note.owner_id == user.id).order_by(Note.id.desc()).all()
    # collect distinct tags for UI
    all_tags_raw = [n.tags for n in db.query(Note).filter(Note.owner_id == user.id).all() if n.tags]
    tag_set = set()
    for t in all_tags_raw:
        parts = [p.strip() for p in t.split(",") if p.strip()]
        tag_set.update(parts)
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes, "user": user, "tags": sorted(tag_set), "selected_tag": tag or ""})

@router.post("/add-note")
def add_note(request: Request,
             title: str = Form(...),
             content: str = Form(""),
             tags: str = Form(""),
             db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    note = Note(title=title.strip(), content=content.strip(), tags=",".join([t.strip() for t in tags.split(",") if t.strip()]), owner_id=user.id)
    db.add(note)
    db.commit()
    return RedirectResponse("/notes", status_code=302)

@router.get("/edit/{note_id}")
def edit_page(note_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        return RedirectResponse("/notes")
    return templates.TemplateResponse("edit_note.html", {"request": request, "note": note})

@router.post("/edit/{note_id}")
def edit_note(note_id: int, request: Request,
              title: str = Form(...),
              content: str = Form(""),
              tags: str = Form(""),
              db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = title.strip()
    note.content = content.strip()
    note.tags = ",".join([t.strip() for t in tags.split(",") if t.strip()])
    db.commit()
    return RedirectResponse("/notes", status_code=302)

@router.get("/delete/{note_id}")
def delete_note(note_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse("/login")
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if note:
        db.delete(note)
        db.commit()
    return RedirectResponse("/notes", status_code=302)
