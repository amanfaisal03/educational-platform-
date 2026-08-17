from sqlalchemy.orm import Session

from app.models import Course, Lesson, Unit


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_courses(self) -> list[Course]:
        return self.db.query(Course).all()

    def get_course_by_id(self, course_id: int) -> Course | None:
        return self.db.query(Course).filter(Course.id == course_id).first()

    def get_course_by_name(self, name: str) -> Course | None:
        return self.db.query(Course).filter(Course.name == name).first()

    def add_course(self, name: str) -> Course:
        course = Course(name=name)
        self.db.add(course)
        self.db.flush()
        self.db.refresh(course)
        return course

    def delete_course(self, course: Course) -> None:
        self.db.delete(course)
        self.db.flush()

    def get_unit_by_id(self, unit_id: int) -> Unit | None:
        return self.db.query(Unit).filter(Unit.id == unit_id).first()

    def add_unit(self, course_id: int, title: str) -> Unit:
        unit = Unit(title=title, course_id=course_id)
        self.db.add(unit)
        self.db.flush()
        self.db.refresh(unit)
        return unit

    def get_lesson_by_title(
        self,
        unit_id: int,
        title: str,
    ) -> Lesson | None:
        return (
            self.db.query(Lesson)
            .filter(
                Lesson.unite_id == unit_id,
                Lesson.title == title,
            )
            .first()
        )

    def add_lesson(self, unit_id: int, title: str) -> Lesson:
        lesson = Lesson(title=title, unite_id=unit_id)
        self.db.add(lesson)
        self.db.flush()
        self.db.refresh(lesson)
        return lesson


__all__ = ["CourseRepository"]
