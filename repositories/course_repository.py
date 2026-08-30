from sqlalchemy.orm import Session

from app.models.course import Course,Lesson, Unit


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_courses(self) -> list[Course]:
        return self.db.query(Course).filter(Course.is_active.is_(True)).all()

    def get_course_by_id(self, course_id: int) -> Course | None:
        return self.db.query(Course).filter(Course.id == course_id ,Course.is_active.is_(True)).first()

    def get_units_by_course_id(self, course_id: int) -> list[Unit] | None:
        return self.db.query(Unit).filter(Unit.course_id == course_id,Unit.is_active.is_(True)).all()

    def get_course_by_name(self, name: str) -> Course | None:
        return self.db.query(Course).filter(Course.name == name).first()

    def add_course(self, name: str) -> Course:
        course = Course(name=name)
        self.db.add(course)
        self.db.flush()
        self.db.refresh(course)
        return course

    def deactivate_course(self, course: Course) -> None:
        course.is_active = False

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
    def get_lessons_by_unit_id(self, unit_id: int) -> list[Lesson] | None:
        return (self.db.query(Lesson).filter(Lesson.unite_id == unit_id,Lesson.unit_id.is_active.is_(True)).all())

    def add_lesson(self, unit_id: int, title: str) -> Lesson:
        lesson = Lesson(title=title, unite_id=unit_id)
        self.db.add(lesson)
        self.db.flush()
        self.db.refresh(lesson)
        return lesson


__all__ = ["CourseRepository"]
