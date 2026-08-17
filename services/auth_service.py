from app.core.password_hasher import hash_password, verify_password
from app.models import User
from app.schemas.auth import LoginRequest, StudentRegistrationRequest
from repositories.user_repository import UserRepository
from services.exceptions import InvalidCredentialsError, UserAlreadyExistsError


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


__all__ = ["AuthService"]
