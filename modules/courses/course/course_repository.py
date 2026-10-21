from sqlalchemy.orm import Session, selectinload

from modules.courses.course.models import Course
from modules.courses.unit.models import Unit
from modules.courses.lesson.models import Lesson
from modules.courses.material.models import Material


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_courses(self, limit: int | None = None, offset: int = 0) -> list[Course]:
        query = (
            self.db.query(Course)
            .filter(Course.is_active.is_(True))
            .order_by(Course.id)
        )
        if limit is not None:
            query = query.offset(offset).limit(limit)
        return query.all()

    def count_courses(self) -> int:
        return self.db.query(Course).filter(Course.is_active.is_(True)).count()

    def get_course_by_id(self, course_id: int) -> Course | None:
        return self.db.query(Course).filter(Course.id == course_id ,Course.is_active.is_(True)).first()

    def get_course_for_player(self, course_id: int) -> Course | None:
        return (
            self.db.query(Course)
            .filter(Course.id == course_id, Course.is_active.is_(True))
            .options(
                selectinload(Course.units.and_(Unit.is_active.is_(True)))
                .selectinload(Unit.lessons.and_(Lesson.is_active.is_(True)))
                .selectinload(Lesson.materials.and_(Material.is_active.is_(True)))
                .load_only(Material.id, Material.lesson_id, Material.type,
                           Material.is_active, raiseload=True)
            )
            .first()
        )

    def get_course_by_name(self, name: str) -> Course | None:
        return self.db.query(Course).filter(Course.name == name).first()

    def add_course(self, name: str , grade_id) -> Course:
        course = Course(name=name, grade_id=grade_id)
        self.db.add(course)
        self.db.flush()
        self.db.refresh(course)
        return course

    def deactivate_course(self, course: Course) -> None:
        course.is_active = False



__all__ = ["CourseRepository"]
