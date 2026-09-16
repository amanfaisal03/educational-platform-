from modules.auth.password_hasher import hash_password, verify_password
from modules.users.student.models import User
from modules.auth.schemas import LoginRequest, StudentRegistrationRequest
from modules.users.admin.repository import AdminRepository
from jose.exceptions import InvalidCredentialsError, UserAlreadyExistsError


class AuthService:
    def __init__(self, users: AdminRepository) -> None:
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
