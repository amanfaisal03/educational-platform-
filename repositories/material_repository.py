from sqlalchemy.orm import Session

from app.models.course import Lesson, Material


class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_lesson(self, lesson_id: int) -> Lesson | None:
        return self.db.query(Lesson).filter(Lesson.id == lesson_id).first()

    def get_by_lesson_and_type(
        self,
        lesson_id: int,
        material_type: str,
    ) -> Material | None:
        return (
            self.db.query(Material)
            .filter(
                Material.lesson_id == lesson_id,
                Material.type == material_type,
            )
            .first()
        )

    def add(
        self,
        lesson_id: int,
        material_type: str,
        file_data: bytes,
    ) -> Material:
        material = Material(
            lesson_id=lesson_id,
            type=material_type,
            file_data=file_data,
        )
        self.db.add(material)
        self.db.flush()
        self.db.refresh(material)
        return material


__all__ = ["MaterialRepository"]
