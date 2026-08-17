from app.models import Course, UserCourse
from repositories.course_repository import CourseRepository
from repositories.user_courses_repository import UserCourseRepository
from services.exceptions import CourseNotFoundError


class EnrollmentService:
    def __init__(
        self,
        courses: CourseRepository,
        enrollments: UserCourseRepository,
    ) -> None:
        self.courses = courses
        self.enrollments = enrollments

    def enroll(self, user_id: int, course_id: int) -> UserCourse:
        if self.courses.get_course_by_id(course_id) is None:
            raise CourseNotFoundError(course_id)

        existing = self.enrollments.get_enrollment(user_id, course_id)
        if existing is not None:
            return existing

        return self.enrollments.add(user_id, course_id)

    def list_courses_for_student(self, user_id: int) -> list[Course]:
        return self.enrollments.list_courses_for_student(user_id)


__all__ = ["EnrollmentService"]
