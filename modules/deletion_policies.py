from typing import Protocol

from modules.users.student.models import User
from modules.users.user_course.user_courses_repository import UserCourseRepository
from modules.users.repository import UserRepository


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
