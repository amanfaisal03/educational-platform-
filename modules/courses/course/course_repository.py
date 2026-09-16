from sqlalchemy.orm import Session

from modules.courses.course.models import Course


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_courses(self) -> list[Course]:
        return self.db.query(Course).filter(Course.is_active.is_(True)).all()

    def get_course_by_id(self, course_id: int) -> Course | None:
        return self.db.query(Course).filter(Course.id == course_id ,Course.is_active.is_(True)).first()

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



__all__ = ["CourseRepository"]
