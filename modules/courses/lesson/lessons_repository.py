from modules.courses.lesson.models import Lesson
from modules.courses.unit.models import Unit
from sqlalchemy.orm import Session


class LessonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_lesson_by_title(
        self,
        unit_id: int,
        title: str,
    ) -> Lesson | None:
        return (
            self.db.query(Lesson)
            .filter(
                Lesson.unit_id == unit_id,
                Lesson.title == title,
            )
            .first()
        )
    def get_lessons_by_unit_id(
        self,
        unit_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Lesson]:
        query = (
            self.db.query(Lesson)
            .filter(
                Lesson.unit_id == unit_id,
                Lesson.is_active.is_(True),
                Lesson.unit.has(Unit.is_active.is_(True)),
            )
            .order_by(Lesson.id)
        )
        if limit is not None:
            query = query.offset(offset).limit(limit)
        return query.all()

    def add_lesson(self, unit_id: int, title: str) -> Lesson:
        lesson = Lesson(title=title, unit_id=unit_id)
        self.db.add(lesson)
        self.db.flush()
        self.db.refresh(lesson)
        return lesson

    def count_lessons(self, unit_id: int) -> int:
        return (
            self.db.query(Lesson)
            .filter(
                Lesson.unit_id == unit_id,
                Lesson.is_active.is_(True),
                Lesson.unit.has(Unit.is_active.is_(True)),
            )
            .count()
        )

    def get_lesson_by_id(self, lesson_id: int) -> Lesson | None:
        return (
            self.db.query(Lesson)
            .filter(
                Lesson.id == lesson_id,
                Lesson.is_active.is_(True),
            )
            .first()
        )



__all__ = ["LessonRepository"]
