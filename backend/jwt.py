from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from pydantic import BaseModel
from Config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

def create_access_token(email: str, user_id: int, role: str) -> str:
    return jwt.encode({"email": email,
                       "user_id": user_id,
                       "role": role},
                      SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> TokenData:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email, user_id = payload.get("email"), payload.get("user_id")
    if not email or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return TokenData(email=email, user_id=user_id)
