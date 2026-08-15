from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.dependencies.authorization import require_admin
from api.dependencies.services import get_material_service
from app.db.database import get_db_session
from app.models import Course, Unit
from services.admin_service import (
    add_course_to_dashbord,
    add_lesson_by_unite,
    add_unite_to_course,
    delete_course_from_dashboard,
)
from services.material_service import (
    EmptyMaterialError,
    InvalidMaterialTypeError,
    LessonNotFoundError,
    MaterialService,
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


async def _upload(
    lesson_id: int,
    file: UploadFile,
    material_type: str,
    service: MaterialService,
):
    file_data = await file.read()
    try:
        result = service.create_material(lesson_id, material_type, file_data)
    except LessonNotFoundError:
        raise HTTPException(status_code=404, detail="Lesson not found")
    except InvalidMaterialTypeError:
        raise HTTPException(status_code=400, detail="Invalid material type")
    except EmptyMaterialError:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    return RedirectResponse(
        f"/admin/units/{result.unit_id}/lessons",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@admin_courses_router.post("/lessons/upload-video")
async def upload_video(lesson_id: int = Form(...),file: UploadFile = File(...),service: MaterialService = Depends(get_material_service),):
    return await _upload(lesson_id, file, "video", service)


@admin_courses_router.post("/lessons/upload-pdf")
async def upload_pdf(lesson_id: int = Form(...),file: UploadFile = File(...),service: MaterialService = Depends(get_material_service),):
    return await _upload(lesson_id, file, "pdf", service)
