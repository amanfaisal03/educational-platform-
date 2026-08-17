from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from api.dependencies.authorization import require_student
from api.dependencies.services import get_enrollment_service
from app.models import User
from services.enrollment_service import EnrollmentService
from services.exceptions import CourseNotFoundError


student_router = APIRouter(
    prefix="/student",
    tags=["Students"],
    dependencies=[Depends(require_student)],
)
templates = Jinja2Templates(directory="templates")


@student_router.get("/mycourses", response_class=HTMLResponse)
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


@student_router.post("/add-course/{course_id}")
def enroll(
    course_id: int,
    student: User = Depends(require_student),
    service: EnrollmentService = Depends(get_enrollment_service),
):
    try:
        service.enroll(student.id, course_id)
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")
    return RedirectResponse(
        "/student/mycourses",
        status_code=status.HTTP_303_SEE_OTHER,
    )
