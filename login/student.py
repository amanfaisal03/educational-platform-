from fastapi import FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from fastapi import Depends
from models.database import get_db_session
from models.schema import Course , Unit ,Lesson ,Material
from fastapi.responses import StreamingResponse
import io

def get_courses_from_dashboard(db: Session = Depends(get_db_session)):
    courses = db.query(Course).all()
    return courses


def get_unite_by_course_id(course_id: int, db: Session = Depends(get_db_session)):
    unite = db.query(Unit).filter_by(course_id=course_id).all()
    return unite


def get_lesson_by_unit_id(unit_id:int,db: Session = Depends(get_db_session)):
    lesson=db.query(Lesson).filter_by(unit_id=unit_id).all()
    return lesson



