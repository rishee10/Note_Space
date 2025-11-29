from pydantic import BaseModel

class NoteCreate(BaseModel):
    topic: str
    description: str

class UserCreate(BaseModel):
    username: str
    password: str
