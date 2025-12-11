from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Truncate to 72 bytes (UTF-8) before hashing
    password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_ctx.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    # Truncate to 72 bytes (UTF-8) before verification
    plain = plain.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_ctx.verify(plain, hashed)


def create_access_token(data: dict, expires_minutes: int = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=(expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return {}
