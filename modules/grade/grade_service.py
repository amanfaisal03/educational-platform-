
from modules.courses.course.course_repository import CourseRepository
from modules.exceptions import EmptyTitleError, GradeAlreadyExistsError
from modules.grade.grade_repo import GradeRepository
from modules.grade.models import Grade


class GradeService:

    def __init__(self, course: CourseRepository, grade: GradeRepository):
        self.course = course
        self.grade = grade

    def list_grades(self) -> list[Grade]:
        return self.grade.list_grades()

    def create_grade(self,  name: str) -> Grade:
        grade_name = name.strip()
        if not grade_name:
            raise EmptyTitleError()
        if self.grade.get_grade_by_name(grade_name) is not None:
            raise GradeAlreadyExistsError(grade_name)
        return self.grade.create_grade(grade_name)


    def get_grade_by_id(self, grade_id: str) -> Grade:
        return self.grade.get_grade_by_id(grade_id)


