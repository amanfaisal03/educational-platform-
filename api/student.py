from fastapi import APIRouter
from starlette.responses import Response
from login.student import get_courses_from_dashboard ,get_unite_by_course_id , get_lesson_by_unit_id

from fastapi import FastAPI, UploadFile, File, Depends ,APIRouter
from sqlalchemy.orm import Session
from models.database import get_db_session
from models.schema import Material
# from config import Settings
student_router = APIRouter(prefix="/student")
@student_router.get("/get_courses")
def get_courses_endpoint(db: Session = Depends(get_db_session)):
    courses = get_courses_from_dashboard(db)
    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "title": course.title
        })
    return result

@student_router.get("/get_units")
def get_unit_by_course_id_endpoint(course_id: int, db: Session = Depends(get_db_session)):
    units = get_unite_by_course_id(course_id, db)
    result = []
    for unit in units:
        result.append({
            "id": unit.id,
            "title": unit.title,
        })
    return result


@student_router.get("/get_lesson")
def get_lesson_endpoint(unit_id:int,db:Session=Depends(get_db_session)):
    lessons=get_lesson_by_unit_id(unit_id,db)
    lessons_by_unit=[]
    for lesson in lessons:
        lessons_by_unit.append({
            "id": lesson.id,
            "title": lesson.title,
        })
    return lessons_by_unit

@student_router.get("/get_video")
def get_video_by_lesson_id(lesson_id: int,db: Session = Depends(get_db_session)):
    video = db.query(Material).filter( Material.lesson_id == lesson_id,Material.type == "video").first()
    if not video:
        return {"error": "Video not found"}

    return Response(
        content=video.file_data,
        media_type="video/mp4"
    )
@student_router.get("/pdf")
def get_pdf_by_lesson_id(lesson_id: int,db: Session = Depends(get_db_session)):
    pdf = db.query(Material).filter(Material.lesson_id == lesson_id,Material.type == "pdf").first()
    if not pdf:
        return {"error": "PDF not found"}

    return Response(
        content=pdf.file_data,
        media_type="application/pdf"
    )
