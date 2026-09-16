from modules.courses.course.course_repository import CourseRepository
from modules.courses.unit.unit_repository import UnitRepository
from jose.exceptions import EmptyTitleError ,UnitNotFoundError
from modules.courses.unit.models import Unit

class UnitService:
    def __init__(self, unit: UnitRepository ,course:CourseRepository):
        self.unit = unit
        self.course = course

    def create_unit(self, course_id: int, title: str) -> Unit:
        normalized_title = title.strip()
        if not normalized_title:
            raise EmptyTitleError()
        self.course.get_course_by_id(course_id)
        return self.unit.add_unit(course_id, normalized_title)


    def get_unit(self, unit_id: int) -> Unit:
        unit = self.unit.get_unit_by_id(unit_id)
        if unit is None or not unit.is_active:
            raise UnitNotFoundError(unit_id)
        return unit


    def get_units_by_course_id(self, course_id: int) -> list[Unit]:
        return self.unit.get_units_by_course_id(course_id)


__all__=["UnitService"]