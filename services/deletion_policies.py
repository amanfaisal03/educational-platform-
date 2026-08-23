from typing import Protocol

from app.models import User
from repositories.user_courses_repository import UserCourseRepository
from repositories.user_repository import UserRepository


class StudentDeletionPolicy(Protocol):
    def delete(self, student: User) -> None:
        pass


class HardDeleteStudentDeletionPolicy:
    def __init__(
        self,
        users: UserRepository,
        enrollments: UserCourseRepository,
    ) -> None:
        self.users = users
        self.enrollments = enrollments

    def delete(self, student: User) -> None:
        self.enrollments.delete_for_student(student.id)
        self.users.delete(student)


class SoftDeleteStudentDeletionPolicy:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def delete(self, student: User) -> None:
        self.users.soft_delete(student)


__all__ = [
    "StudentDeletionPolicy",
    "SoftDeleteStudentDeletionPolicy",
    "HardDeleteStudentDeletionPolicy",
]
