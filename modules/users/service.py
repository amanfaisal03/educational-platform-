from typing import Protocol

from fastapi import Depends
from sqlalchemy.orm import Session

from modules.database import get_db_session
from modules.exceptions import StudentNotFoundError
from modules.users.student.models import User
from modules.users.repository import UserRepository
from modules.pagination import  pagination

class StudentDeletionPolicy(Protocol):
    def delete(self, student: User) -> None:
        pass


class SoftDeleteStudentDeletionPolicy:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def delete(self, student: User) -> None:
        self.users.soft_delete(student)


class HardDeleteStudentDeletionPolicy:
    def __init__(self, users: UserRepository, enrollments) -> None:
        self.users = users
        self.enrollments = enrollments

    def delete(self, student: User) -> None:
        self.enrollments.delete_for_student(student.id)
        self.users.delete(student)


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

    def list_students_paginated(
        self,
        page: int,
        per_page: int,
    ) -> tuple[list[User], int, int]:
        total = self.users.count_students()
        page, total_pages, offset = pagination.calculate_pagination(
            total, page, per_page
        )
        students = self.users.list_students(limit=per_page, offset=offset)
        return students, page, total_pages

    def get_student(self, student_id: int) -> User | None:
        return self.users.get_student_by_id(student_id)

    def delete_student(self, student_id: int) -> None:
        student = self.users.get_student_by_id(student_id)
        if student is None:
            raise StudentNotFoundError()
        self.deletion_policy.delete(student)
    def count_students(self) -> int:
        return self.users.count_students()

def get_student_admin_service(
    db: Session = Depends(get_db_session),
) -> StudentAdminService:
    users = UserRepository(db)
    return StudentAdminService(
        users=users,
        deletion_policy=SoftDeleteStudentDeletionPolicy(users),
    )


__all__ = [
    "StudentDeletionPolicy",
    "SoftDeleteStudentDeletionPolicy",
    "HardDeleteStudentDeletionPolicy",
    "StudentAdminService",
    "get_student_admin_service",
]
