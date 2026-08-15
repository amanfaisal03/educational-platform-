from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.dependencies.authorization import require_student
from app.db.database import get_db_session
from app.models import Course, User, UserCourse
from services.student_service import get_courses_for_each_student


student_router = APIRouter(
    prefix="/student",
    tags=["Students"],
    dependencies=[Depends(require_student)],
)
templates = Jinja2Templates(directory="templates")


@student_router.get("/mycourses", response_class=HTMLResponse)
def display_my_courses(
    request: Request,
    db: Session = Depends(get_db_session),
    student: User = Depends(require_student),
):
    return templates.TemplateResponse(
        request=request,
        name="student/mycourses.html",
        context={"courses": get_courses_for_each_student(student.id, db)},
    )


@student_router.post("/add-course/{course_id}")
def enroll(
    course_id: int,
    db: Session = Depends(get_db_session),
    student: User = Depends(require_student),
):
    if db.query(Course).filter(Course.id == course_id).first() is None:
        raise HTTPException(status_code=404, detail="Course not found")
    existing = db.query(UserCourse).filter(
        UserCourse.user_id == student.id,
        UserCourse.course_id == course_id,
    ).first()
    if existing is None:
        db.add(UserCourse(user_id=student.id, course_id=course_id))
        db.commit()
    return RedirectResponse("/student/mycourses", status_code=status.HTTP_303_SEE_OTHER)
