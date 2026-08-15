from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.dependencies.authorization import require_admin
from app.db.database import get_db_session
from app.models import Course, Lesson, Unit
from services.admin_service import (
    add_course_to_dashbord,
    add_lesson_by_unite,
    add_unite_to_course,
    delete_course_from_dashboard,
    upload_material,
)
from services.student_service import get_courses_from_dashboard


admin_courses_router = APIRouter(
    prefix="/admin",
    tags=["Admin courses"],
    dependencies=[Depends(require_admin)],
)
templates = Jinja2Templates(directory="templates")


@admin_courses_router.get("/courses", response_class=HTMLResponse)
def display_courses(request: Request, db: Session = Depends(get_db_session)):
    return templates.TemplateResponse(
        request=request,
        name="admin/courses.html",
        context={"courses": get_courses_from_dashboard(db)},
    )


@admin_courses_router.post("/add_courses")
def create_course(title: str = Form(...), db: Session = Depends(get_db_session)):
    add_course_to_dashbord(title, db)
    return RedirectResponse("/admin/courses", status_code=status.HTTP_303_SEE_OTHER)


@admin_courses_router.post("/courses/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db_session)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    delete_course_from_dashboard(course_id, db)
    return RedirectResponse("/admin/courses", status_code=status.HTTP_303_SEE_OTHER)


@admin_courses_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def display_course_units(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db_session),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse(
        request=request,
        name="admin/units.html",
        context={"course": course},
    )


@admin_courses_router.post("/units")
def create_course_unit(
    course_id: int = Form(...),
    title: str = Form(...),
    db: Session = Depends(get_db_session),
):
    if db.query(Course).filter(Course.id == course_id).first() is None:
        raise HTTPException(status_code=404, detail="Course not found")
    add_unite_to_course(course_id, title, db)
    return RedirectResponse(
        f"/admin/courses/{course_id}/units",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@admin_courses_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def display_unit_lessons(
    request: Request,
    unit_id: int,
    db: Session = Depends(get_db_session),
):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return templates.TemplateResponse(
        request=request,
        name="admin/lessons.html",
        context={"unit": unit},
    )


@admin_courses_router.post("/lessons")
def create_unit_lesson(
    unit_id: int = Form(...),
    title: str = Form(...),
    db: Session = Depends(get_db_session),
):
    if db.query(Unit).filter(Unit.id == unit_id).first() is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    add_lesson_by_unite(unit_id, title, db)
    return RedirectResponse(
        f"/admin/units/{unit_id}/lessons",
        status_code=status.HTTP_303_SEE_OTHER,
    )


def _upload(lesson_id: int, file: UploadFile, material_type: str, db: Session):
    if db.query(Lesson).filter(Lesson.id == lesson_id).first() is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return upload_material(lesson_id, file, material_type, db)


@admin_courses_router.post("/lessons/upload-video")
def upload_video(
    lesson_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
):
    return _upload(lesson_id, file, "video", db)


@admin_courses_router.post("/lessons/upload-pdf")
def upload_pdf(
    lesson_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
):
    return _upload(lesson_id, file, "pdf", db)
