import hashlib
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # pre-hash long password using SHA256
    sha256 = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha256)

def verify_password(password, hashed):
    sha256 = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.verify(sha256, hashed)

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=24)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
