from sqlalchemy.orm import Session
from app.models import Lesson, Material, Course, Unit, UserCourse


class CourseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_lessons(self, lesson_id: int) -> Lesson | None:
        lesson=self.db.query(Lesson).filter(Lesson.id == lesson_id).first()
        return lesson

    def get_unite_by_course_id(self, course_id: int):
        courses = self.db.query(Course).filter(Course.id == course_id).first()
        return courses

    def get_courses_from_dashboard(self):
        courses = self.db.query(Course).all()
        return courses

    def get_lesson_by_unit_id(self,unite_id: int):
        unite = self.db.query(Unit).filter(Unit.id == unite_id).first()
        return unite

    def get_courses_for_each_student(self,user_id):
        courses = self.db.query(Course).join(UserCourse, Course.id == UserCourse.course_id).filter(
            UserCourse.user_id == user_id).all()
        return courses




__all__=['CourseRepository']