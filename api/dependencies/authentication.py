from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status

from api.dependencies.services import get_auth_service, get_token_service
from app.models import User
from services.auth_service import AuthService
from services.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    MissingTokenSubjectError,
)
from services.token_service import TokenService


def get_current_user(
    authorization: Optional[str] = Cookie(None),
    auth_service: AuthService = Depends(get_auth_service),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in, please sign in",
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
        )

    token = authorization.removeprefix("Bearer ")
    try:
        token_data = token_service.decode_access_token(token)
    except ExpiredTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except (InvalidTokenError, MissingTokenSubjectError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = auth_service.get_user_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
