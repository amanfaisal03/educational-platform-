from dataclasses import dataclass

from app.models import Material
from repositories.material_repository import MaterialRepository


class LessonNotFoundError(Exception):
    """Raised when material is uploaded for a lesson that does not exist."""


class InvalidMaterialTypeError(Exception):
    """Raised when the material type is not supported."""


class EmptyMaterialError(Exception):
    """Raised when the uploaded file has no content."""


@dataclass(frozen=True)
class MaterialCreationResult:
    material: Material
    unit_id: int


class MaterialService:
    ALLOWED_TYPES = {"pdf", "video"}

    def __init__(self, repository: MaterialRepository):
        self.repository = repository

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
            Material(
                lesson_id=lesson_id,
                type=material_type,
                file_data=file_data,
            )
        )
        return MaterialCreationResult(material=material, unit_id=lesson.unite_id)
