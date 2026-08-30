from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse

from api.dependencies.authorization import require_student
from api.dependencies.services import get_course_service, get_enrollment_service
from app.models.user import User
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.exceptions import CourseNotFoundError, UnitNotFoundError


student_courses_router = APIRouter(
    prefix="/api/v1/student",
    tags=["APi V1 - Student courses"],
    dependencies=[Depends(require_student)],
)

templates = Jinja2Templates(directory="templates")

@student_courses_router.get("/allcourses", response_class=HTMLResponse)
def display_all_courses(
    request: Request,
    service: CourseService = Depends(get_course_service),
):
    return templates.TemplateResponse(
        request=request,
        name="student/allcourses.html",
        context={"courses": service.list_courses()},
    )


@student_courses_router.get("/mycourses", response_class=HTMLResponse)
def display_my_courses(
    request: Request,
    student: User = Depends(require_student),
    service: EnrollmentService = Depends(get_enrollment_service),
):
    return templates.TemplateResponse(
        request=request,
        name="student/mycourses.html",
        context={"courses": service.list_courses_for_student(student.id)},
    )


@student_courses_router.post("/buy-course/{course_id}")
def buy_course(
    course_id: int,
    student: User = Depends(require_student),
    service: EnrollmentService = Depends(get_enrollment_service),
):
    try:
        service.buy_course(student.id, course_id)
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")
    return RedirectResponse(
        "/api/v1/student/mycourses",
        status_code=status.HTTP_303_SEE_OTHER,
    )

@student_courses_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def display_course_units(
    request: Request,
    course_id: int,
    service: CourseService = Depends(get_course_service),
):
    try:
        course = service.get_units_by_course_id(course_id)
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse(
        request=request,
        name="student/units.html",
        context={"course": course},
    )

@student_courses_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def display_course_units(
    request: Request,
    course_id: int,
    service: CourseService = Depends(get_course_service),
):
    try:
        course = service.get_course(course_id)
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse(
        request=request,
        name="admin/units.html",
        context={"course": course},
    )

@student_courses_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def display_unit_lessons(
    request: Request,
    unit_id: int,
    service: CourseService = Depends(get_course_service),
):
    try:
        unit = service.get_unit(unit_id)
    except UnitNotFoundError:
        raise HTTPException(status_code=404, detail="Unit not found")
    return templates.TemplateResponse(
        request=request,
        name="student/lessons.html",
        context={"unite": unit},
    )


