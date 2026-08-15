"""

app/core/security.py
├── Password hashing
├── Password verification
├── JWT creation
└── JWT verification

"""
import datetime
from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from app.core.Config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def JWT_creation(user_id: int) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

def JWT_verification(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        subject = payload.get("sub")

        if subject is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )
        return TokenData(user_id=int(subject))

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )
