import datetime

from fastapi import Depends
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session

from modules.users.repository import UserRepository
from modules.auth.schemas import LoginRequest, StudentRegistrationRequest, TokenData
from modules.Config import settings
from modules.auth.password_hasher import hash_password, verify_password
from modules.database import get_db_session
from jose.exceptions import ExpiredTokenError,InvalidCredentialsError,InvalidTokenError,MissingTokenSubjectError,UserAlreadyExistsError
from modules.users.student.models import User


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.users.get_user_by_id(user_id)

    def register_student(self, request: StudentRegistrationRequest) -> User:
        email = request.email.lower().strip()
        if self.users.get_user_by_email(email):
            raise UserAlreadyExistsError()

        return self.users.add(
            name=request.name.strip(),
            email=email,
            password=hash_password(request.password),
            role="student",
        )

    def authenticate(self, request: LoginRequest) -> User:
        email = request.email.lower().strip()
        user = self.users.get_user_by_email(email)

        if user is None or not verify_password(request.password, user.password):
            raise InvalidCredentialsError()

        return user



class TokenService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        expire_minutes: int,
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    @classmethod
    def from_settings(cls) -> "TokenService":
        return cls(
            secret_key=settings.secret_key,
            algorithm=settings.jwt_algorithm,
            expire_minutes=settings.access_token_expire_minutes,
        )

    def create_access_token(self, user_id: int) -> str:
        expires_at = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(minutes=self.expire_minutes)
        payload = {"sub": str(user_id), "exp": expires_at}
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
        except ExpiredSignatureError as exc:
            raise ExpiredTokenError() from exc
        except JWTError as exc:
            raise InvalidTokenError() from exc

        subject = payload.get("sub")
        if subject is None:
            raise MissingTokenSubjectError()

        try:
            return TokenData(user_id=int(subject))
        except (TypeError, ValueError) as exc:
            raise InvalidTokenError() from exc


def get_auth_service(db: Session = Depends(get_db_session)) -> AuthService:
    return AuthService(UserRepository(db))


def get_token_service() -> TokenService:
    return TokenService.from_settings()


__all__ = [
    "AuthService",
    "TokenService",
    "get_auth_service",
    "get_token_service",
]
