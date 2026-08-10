from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import Response, HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from services.student_service import get_courses_from_dashboard,get_unite_by_course_id,get_lesson_by_unit_id,get_courses_for_each_student
from app.db.database import get_db_session
from app.db.schema import Material,User ,UserCourse
from services.auth_service import get_current_user, get_student_names
from fastapi.responses import RedirectResponse

student_router = APIRouter(prefix="/students",tags=["Students"],dependencies=[Depends(get_current_user)],)
templates = Jinja2Templates(directory="templates")

@student_router.get("/allcourses", response_class=HTMLResponse)
def get_courses_page(request: Request, db: Session = Depends(get_db_session)):
    courses = get_courses_from_dashboard(db)
    return templates.TemplateResponse(request, "student/allcourses.html", {"courses": courses})

@student_router.get("/mycourses", response_class=HTMLResponse)
def my_courses(request: Request,db: Session = Depends(get_db_session),user: User = Depends(get_current_user)):
    courses = get_courses_for_each_student(user.id, db)

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

