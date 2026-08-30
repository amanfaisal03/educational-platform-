from app.models import Course, Lesson, Unit
from repositories.course_repository import CourseRepository
from services.exceptions import (
    CourseAlreadyExistsError,
    CourseNotFoundError,
    EmptyTitleError,
    LessonAlreadyExistsError,
    UnitNotFoundError, LessonNotFoundError,
)


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



    def create_unit(self, course_id: int, title: str) -> Unit:
        normalized_title = title.strip()
        if not normalized_title:
            raise EmptyTitleError()
        self.get_course(course_id)
        return self.courses.add_unit(course_id, normalized_title)

    def create_lesson(self, unit_id: int, title: str) -> Lesson:
        normalized_title = title.strip()
        if not normalized_title:
            raise EmptyTitleError()
        self.get_units_by_course_id(unit_id)
        if self.courses.get_lesson_by_title(unit_id, normalized_title) is not None:
            raise LessonAlreadyExistsError(normalized_title)
        return self.courses.add_lesson(unit_id, normalized_title)


    def get_units_by_course_id(self, course_id: int) -> list[Unit]:
        units = self.courses.get_units_by_course_id(course_id)
        if units is None:
            raise UnitNotFoundError(course_id)
        return units

    def get_lessons_by_unit_id(self, unit_id: int) -> list[Lesson]:
        lesson=self.courses.get_lessons_by_unit_id(unit_id)
        if lesson is None:
            raise LessonNotFoundError(unit_id)
        return lesson




__all__ = ["CourseService"]
