from modules.courses.lesson.models import Lesson
from modules.courses.lesson.lessons_repository import LessonRepository
from modules.courses.unit.unit_repository import UnitRepository
from jose.exceptions import EmptyTitleError ,LessonAlreadyExistsError



class LessonService:
    def __init__(self, lesson: LessonRepository , unit:UnitRepository):
        self.lesson = lesson
        self.unit = unit

    def create_lesson(self, unit_id: int, title: str) -> Lesson:
        normalized_title = title.strip()
        if not normalized_title:
            raise EmptyTitleError()
        self.unit.get_unit_by_id(unit_id)
        if self.lesson.get_lesson_by_title(unit_id, normalized_title) is not None:
            raise LessonAlreadyExistsError(normalized_title)
        return self.lesson.add_lesson(unit_id, normalized_title)


    def get_lessons_by_unit_id(self, unit_id: int) -> list[Lesson]:
        self.unit.get_unit_by_id(unit_id)
        return self.lesson.get_lessons_by_unit_id(unit_id)



__all__=["LessonService"]