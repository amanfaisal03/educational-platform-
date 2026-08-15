from sqlalchemy.orm import Session

from app.models import Lesson, Material


class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_lesson(self, lesson_id: int) -> Lesson | None:
        return self.db.query(Lesson).filter(Lesson.id == lesson_id).first()

    def add(self, material: Material) -> Material:
        self.db.add(material)
        self.db.flush()
        self.db.refresh(material)
        return material


__all__ = ["MaterialRepository"]
