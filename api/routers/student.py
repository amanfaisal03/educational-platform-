from fastapi import APIRouter, Depends, Request
from fastapi.responses import  HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from api.dependencies.authorization import require_student
from app.models import UserCourse
from services.auth_service import get_student_names
from services.student_service import get_courses_from_dashboard,get_courses_for_each_student
from app.db.database import get_db_session
from app.models.user import User
from api.dependencies.authentication import get_current_user
from fastapi.responses import RedirectResponse

student_router = APIRouter(prefix="/students",tags=["Students"],dependencies=[Depends(require_student)],)
templates = Jinja2Templates(directory="templates")

@student_router.get("/allcourses", response_class=HTMLResponse)
def get_courses_page(request: Request, db: Session = Depends(get_db_session)):
    courses = get_courses_from_dashboard(db)
    return templates.TemplateResponse(request, "student/allcourses.html", {"courses": courses})

@student_router.get("/me/courses", response_class=HTMLResponse)
def get_my_courses(request: Request,db: Session = Depends(get_db_session),current_student: User = Depends(require_student)):
    courses = get_courses_for_each_student(current_student.id, db)
    return templates.TemplateResponse(
        request=request,
        name="student/mycourses.html",
        context={"courses": courses}
    )

@student_router.post("/add-course/{course_id}")
def add_course(course_id: int,db: Session = Depends(get_db_session),user: User = Depends(get_current_user)):
    existing = db.query(UserCourse).filter(UserCourse.user_id == user.id,UserCourse.course_id == course_id).first()
    if not existing:
        db.add(UserCourse(
            user_id=user.id,
            course_id=course_id
        ))
        db.commit()

    return RedirectResponse(url="/student/mycourses", status_code=303)


@student_router.get("/students", response_class=HTMLResponse)
def get_students(request: Request, db: Session = Depends(get_db_session)):
    students = get_student_names(db)
    return templates.TemplateResponse(request, "admin/admin_core_page.html", {"students": students})

