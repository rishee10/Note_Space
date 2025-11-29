from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class NoteBase(BaseModel):
    title: str
    content: Optional[str] = ""
    tags: Optional[str] = ""  # comma-separated

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
