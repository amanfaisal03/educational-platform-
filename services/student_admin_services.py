from app.models import User
from repositories.user_repository import UserRepository
from services.deletion_policies import StudentDeletionPolicy
from services.exceptions import StudentNotFoundError


class StudentAdminService:
    def __init__(
        self,
        users: UserRepository,
        deletion_policy: StudentDeletionPolicy,
    ) -> None:
        self.users = users
        self.deletion_policy = deletion_policy

    def list_students(self) -> list[User]:
        return self.users.list_students()

    def get_student(self, student_id: int) -> User | None:
        return self.users.get_student_by_id(student_id)

    def delete_student(self, student_id: int) -> None:
        student = self.users.get_student_by_id(student_id)
        if student is None:
            raise StudentNotFoundError()
        self.deletion_policy.delete(student)



__all__ = ["StudentAdminService"]
