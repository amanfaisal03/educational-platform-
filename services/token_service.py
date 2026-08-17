import datetime

from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from app.core.Config import settings
from app.schemas.token import TokenData
from services.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    MissingTokenSubjectError,
)


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


__all__ = ["TokenService"]
