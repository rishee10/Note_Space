import hashlib
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "CHANGE_THIS_TO_A_RANDOM_SECRET"  # <-- change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _sha256_prehash(password: str) -> str:
    # ensures bcrypt receives fixed-length input to support arbitrarily long passwords
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def hash_password(password: str) -> str:
    ph = _sha256_prehash(password)
    return pwd_context.hash(ph)

def verify_password(password: str, hashed: str) -> bool:
    ph = _sha256_prehash(password)
    return pwd_context.verify(ph, hashed)

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_HOURS):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
