from dataclasses import dataclass

from app.models import Material
from repositories.material_repository import MaterialRepository
from services.exceptions import (
    EmptyMaterialError,
    InvalidMaterialTypeError,
    LessonNotFoundError,
)


@dataclass(frozen=True)
class MaterialCreationResult:
    material: Material
    unit_id: int


class MaterialService:
    ALLOWED_TYPES = {"pdf", "video"}

    def __init__(self, repository: MaterialRepository):
        self.repository = repository

    def get_material(self, lesson_id: int, material_type: str) -> Material:
        if material_type not in self.ALLOWED_TYPES:
            raise InvalidMaterialTypeError(material_type)

        material = self.repository.get_by_lesson_and_type(
            lesson_id,
            material_type,
        )
        if material is None or material.file_data is None:
            raise LessonNotFoundError(lesson_id)
        return material

    def create_material(
        self,
        lesson_id: int,
        material_type: str,
        file_data: bytes,
    ) -> MaterialCreationResult:
        if material_type not in self.ALLOWED_TYPES:
            raise InvalidMaterialTypeError(material_type)
        if not file_data:
            raise EmptyMaterialError()

        lesson = self.repository.get_lesson(lesson_id)
        if lesson is None:
            raise LessonNotFoundError(lesson_id)

        material = self.repository.add(
            lesson_id=lesson_id,
            material_type=material_type,
            file_data=file_data,
        )
        return MaterialCreationResult(material=material, unit_id=lesson.unite_id)


__all__ = ["MaterialCreationResult", "MaterialService"]
