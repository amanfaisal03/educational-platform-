from typing import Protocol

from app.models import Course, UserCourse
from services.exceptions import CourseNotFoundError


class CourseLookup(Protocol):
    def get_course_by_id(self, course_id: int) -> Course | None:
        ...


class EnrollmentStore(Protocol):
    def get_enrollment(
        self,
        user_id: int,
        course_id: int,
    ) -> UserCourse | None:
        ...

    def add(self, user_id: int, course_id: int) -> UserCourse:
        ...

    def list_courses_for_student(self, user_id: int) -> list[Course]:
        ...


class EnrollmentService:
    def __init__(
        self,
        courses: CourseLookup,
        enrollments: EnrollmentStore,
    ) -> None:
        self.courses = courses
        self.enrollments = enrollments

    def buy_course(self, user_id: int, course_id: int) -> UserCourse:
        if self.courses.get_course_by_id(course_id) is None:
            raise CourseNotFoundError(course_id)

        existing = self.enrollments.get_enrollment(user_id, course_id)
        if existing is not None:
            return existing

        return self.enrollments.add(user_id, course_id)

    def list_courses_for_student(self, user_id: int) -> list[Course]:
        return self.enrollments.list_courses_for_student(user_id)


__all__ = ["CourseLookup", "EnrollmentStore", "EnrollmentService"]
