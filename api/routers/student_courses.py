from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.dependencies.authorization import require_student
from app.db.database import get_db_session
from services.student_service import (
    get_courses_from_dashboard,
    get_lesson_by_unit_id,
    get_unite_by_course_id,
)


student_courses_router = APIRouter(
    prefix="/student",
    tags=["Student courses"],
    dependencies=[Depends(require_student)],
)
templates = Jinja2Templates(directory="templates")


@student_courses_router.get("/allcourses", response_class=HTMLResponse)
def display_all_courses(request: Request, db: Session = Depends(get_db_session)):
    return templates.TemplateResponse(
        request=request,
        name="student/allcourses.html",
        context={"courses": get_courses_from_dashboard(db)},
    )


@student_courses_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def display_course_units(
    request: Request,
    course_id: int,
    db: Session = Depends(get_db_session),
):
    course = get_unite_by_course_id(course_id, db)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse(
        request=request,
        name="student/units.html",
        context={"course": course},
    )


@student_courses_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def display_unit_lessons(
    request: Request,
    unit_id: int,
    db: Session = Depends(get_db_session),
):
    unit = get_lesson_by_unit_id(unit_id, db)
    if unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return templates.TemplateResponse(
        request=request,
        name="student/lessons.html",
        context={"unite": unit},
    )
