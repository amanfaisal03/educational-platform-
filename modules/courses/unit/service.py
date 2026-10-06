
from modules.courses.course.course_repository import CourseRepository
from modules.courses.unit.models import Unit
from modules.courses.unit.unit_repository import UnitRepository
from modules.exceptions import (
    CourseNotFoundError,
    EmptyTitleError,
    UnitNotFoundError,
)
from modules.pagination import pagination
class UnitService:
    def __init__(self, unit: UnitRepository, course: CourseRepository):
        self.unit = unit
        self.course = course

    def create_unit(self, course_id: int, title: str) -> Unit:
        normalized_title = title.strip()
        if not normalized_title:
            raise EmptyTitleError()
        if self.course.get_course_by_id(course_id) is None:
            raise CourseNotFoundError(course_id)
        return self.unit.add_unit(course_id, normalized_title)

    def get_unit(self, unit_id: int) -> Unit:
        unit = self.unit.get_unit_by_id(unit_id)
        if unit is None:
            raise UnitNotFoundError(unit_id)
        return unit

    def get_units_by_course_id_paginated(
        self,
        course_id: int,
        page: int,
        per_page: int,
    ) -> tuple[list[Unit], int, int]:
        total = self.unit.count_units(course_id)
        page, total_pages, offset =pagination.calculate_pagination(
            total, page, per_page
        )
        units = self.unit.get_units_by_course_id(
            course_id,
            limit=per_page,
            offset=offset,
        )
        return units, page, total_pages


__all__ = ["UnitService"]
