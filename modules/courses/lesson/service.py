from modules.courses.lesson.models import Lesson
from modules.courses.lesson.lessons_repository import LessonRepository
from modules.courses.unit.unit_repository import UnitRepository
from modules.courses.unit.models import Unit
from modules.exceptions import (
    EmptyTitleError,
    LessonAlreadyExistsError,
    UnitNotFoundError,
)
from modules.pagination import pagination
class LessonService:
    def __init__(self, lesson: LessonRepository, unit: UnitRepository):
        self.lesson = lesson
        self.unit = unit

    def create_lesson(self, unit_id: int, title: str) -> Lesson:
        normalized_title = title.strip()
        if not normalized_title:
            raise EmptyTitleError()
        if self.unit.get_unit_by_id(unit_id) is None:
            raise UnitNotFoundError(unit_id)
        if self.lesson.get_lesson_by_title(unit_id, normalized_title) is not None:
            raise LessonAlreadyExistsError(normalized_title)
        return self.lesson.add_lesson(unit_id, normalized_title)

    def get_lesson_by_ids(self, lesson_id: int) -> Lesson | None:
        return self.lesson.get_lesson_by_id(lesson_id)

    def get_unit(self, unit_id: int) -> Unit:
        unit = self.unit.get_unit_by_id(unit_id)
        if unit is None:
            raise UnitNotFoundError(unit_id)
        return unit

    def get_lessons_by_unit_id_paginated(
        self,
        unit_id: int,
        page: int,
        per_page: int,
    ) -> tuple[list[Lesson], int, int]:
        self.get_unit(unit_id)
        total = self.lesson.count_lessons(unit_id)
        page, total_pages, offset =pagination.calculate_pagination(
            total, page, per_page
        )
        lessons = self.lesson.get_lessons_by_unit_id(
            unit_id,
            limit=per_page,
            offset=offset,
        )
        return lessons, page, total_pages


__all__ = ["LessonService"]
