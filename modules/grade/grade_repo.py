from fastapi import HTTPException
from modules.courses.course.models import Course
from modules.grade.models import Grade
from sqlalchemy.orm import Session
from modules.courses.course.course_repository import CourseRepository

class GradeRepository:
    def __init__(self, db: Session, Course: CourseRepository):
        self.Course = Course
        self.db = db

    def get_grade_by_name(self, name: str) -> Grade:
        return self.db.query(Grade).filter(Grade.name == name).first()

    def list_grades(self) -> list[Grade]:
        return self.db.query(Grade).order_by(Grade.name).all()

    def create_grade(self, grade_name: str):
        grade_name = Grade(name=grade_name)
        self.db.add(grade_name)
        self.db.flush()
        self.db.refresh(grade_name)
        return grade_name

    def get_grade_by_id(self, grade_id: int) -> Grade:
        return self.db.query(Grade).filter(Grade.id == grade_id).first()

    def link_course_id_with_grade_id(self, course_id: int, grade_id: int):
        course = self.Course.get_course_by_id(course_id)
        grade=self.db.query(Grade).filter(Grade.id == grade_id).first()
        if not course:
            raise HTTPException(404, "Course not found")

        if not grade:
            raise HTTPException(404, "Grade not found")
        course.grade_id = grade_id
        self.db.commit()
        self.db.refresh(course)
        return course
