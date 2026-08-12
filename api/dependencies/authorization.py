"""

api/dependencies/authorization.py
├── require_admin
└── require_student


"""
from fastapi import HTTPException, Depends
from sqlalchemy.sql.functions import current_user

from api.dependencies.authentication import get_current_user
from app.models import User


def require_admin(
        current_user: User = Depends(get_current_user),) -> User:
        if current_user.role != "admin":
            raise HTTPException(status_code=403 , detail="admin access required")
        return current_user


def require_student(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "student":
        raise HTTPException(status_code=403 , detail="student access required")
    return current_user




