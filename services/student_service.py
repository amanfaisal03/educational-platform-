from fastapi import FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.database import get_db_session
from app.models import Course, Unit, Lesson, Material, UserCourse, User
from fastapi.responses import StreamingResponse
import io


def get_courses_from_dashboard(db: Session = Depends(get_db_session)):
    courses = db.query(Course).all()
    return courses

def get_unite_by_course_id(course_id: int, db: Session = Depends(get_db_session)):
    courses = db.query(Course).filter(Course.id==course_id).first()
    # unite = db.query(Unit).filter_by(course_id=course_id).all()
    return courses


def get_lesson_by_unit_id(unite_id:int,db: Session = Depends(get_db_session)):
    unite=db.query(Unit).filter(Unit.id==unite_id).first()
    # lesson=db.query(Lesson).filter_by(unite_id=unite_id).all()
    return unite


def get_courses_for_each_student(user_id, db: Session):
    courses =db.query(Course).join(UserCourse, Course.id == UserCourse.course_id).filter(UserCourse.user_id == user_id).all()
    return courses
