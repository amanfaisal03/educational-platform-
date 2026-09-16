from modules.courses.course.course_repository import CourseRepository
from modules.courses.course.models import Course
from jose.exceptions import CourseNotFoundError ,EmptyTitleError,CourseAlreadyExistsError

class CourseService:
    def __init__(self, courses: CourseRepository):
        self.courses = courses

    def list_courses(self) -> list[Course]:
        return self.courses.list_courses()

    def get_course(self, course_id: int) -> Course:
        course = self.courses.get_course_by_id(course_id)
        if course is None:
            raise CourseNotFoundError(course_id)
        return course

    def create_course(self, name: str) -> Course:
        normalized_name = name.strip()
        if not normalized_name:
            raise EmptyTitleError()
        if self.courses.get_course_by_name(normalized_name) is not None:
            raise CourseAlreadyExistsError(normalized_name)
        return self.courses.add_course(normalized_name)

    def deactivate_course(self, course_id: int) -> None:
        course = self.get_course(course_id)
        self.courses.deactivate_course(course)


__all__=["CourseService"]