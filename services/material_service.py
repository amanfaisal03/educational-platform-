from typing import Protocol

from app.models import Material
from repositories.material_repository import MaterialRepository
from repositories.user_courses_repository import UserCourseRepository
from services.exceptions import (
    CourseAccessDeniedError,
    EmptyMaterialError,
    InvalidMaterialTypeError,
    LessonNotFoundError,
)


class MaterialCreationResult:
    def __init__(self, material: Material, unit_id: int):
        self.material = material
        self.unit_id = unit_id


class MaterialServiceContract(Protocol):
    ALLOWED_TYPES: set[str]

    def get_material(
        self,
        lesson_id: int,
        material_type: str,
        student_id: int | None = None,
    ) -> Material:
        ...

    def create_material(
        self,
        lesson_id: int,
        material_type: str,
        file_data: bytes,
    ) -> MaterialCreationResult:
        ...


class MaterialService(MaterialServiceContract):

    ALLOWED_TYPES = {"pdf", "video"}
    def __init__(
        self,
        repository: MaterialRepository,
        enrollments: UserCourseRepository,
    ):
        self.repository = repository
        self.enrollments = enrollments

    def get_material(
        self,
        lesson_id: int,
        material_type: str,
        student_id: int | None = None,
    ) -> Material:
        if material_type not in self.ALLOWED_TYPES:
            raise InvalidMaterialTypeError(material_type)

        if student_id is not None:
            lesson = self.repository.get_lesson(lesson_id)
            if lesson is None:
                raise LessonNotFoundError(lesson_id)
            if self.enrollments.get_enrollment(
                student_id,
                lesson.unit.course.id,
            ) is None:
                raise CourseAccessDeniedError()

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


__all__ = ["MaterialCreationResult", "MaterialService","MaterialServiceContract"]
