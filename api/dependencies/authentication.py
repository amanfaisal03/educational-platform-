"""api/dependencies/authentication.py
└── get_current_user
"""
from typing import Optional
from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db_session
from app.db.schema import User
from app.core.security import  JWT_verification



def get_current_user(authorization: Optional[str] = Cookie(None), db: Session = Depends(get_db_session)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not logged in, please sign in")

    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token format")

        token = authorization.replace("Bearer ", "")
        token_data = JWT_verification(token)

        user = db.query(User).filter(User.id == token_data.user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")