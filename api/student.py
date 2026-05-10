from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import Response, HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from login.student import get_courses_from_dashboard,get_unite_by_course_id,get_lesson_by_unit_id,get_courses_for_each_student
from models.database import get_db_session
from models.schema import Material,User ,UserCourse
from login.sign_up import get_current_user
from fastapi.responses import RedirectResponse



student_router = APIRouter(prefix="/student")
templates = Jinja2Templates(directory="templates")


@student_router.get("/allcourses", response_class=HTMLResponse)
def get_courses_page(request: Request, db: Session = Depends(get_db_session), user: User = Depends(get_current_user)):
    courses = get_courses_from_dashboard(db)
    return templates.TemplateResponse(request, "student/allcourses.html", {"courses": courses})


@student_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def get_units_page(request: Request, course_id: int, db: Session = Depends(get_db_session),user: User = Depends(get_current_user)):
    units = get_unite_by_course_id(course_id, db)
    return templates.TemplateResponse(request, "student/units.html", {"units": units, "course_id": course_id})


@student_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def get_lessons_page(request: Request, unit_id: int, db: Session = Depends(get_db_session),user: User = Depends(get_current_user)):
    lessons = get_lesson_by_unit_id(unit_id, db)
    return templates.TemplateResponse(request, "student/lessons.html", {"lessons": lessons, "unit_id": unit_id})


@student_router.get("/lessons/{lesson_id}/video")
def get_video(lesson_id: int, db: Session = Depends(get_db_session),user: User = Depends(get_current_user)):
    video = db.query(Material).filter(Material.lesson_id == lesson_id, Material.type == "video").first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return Response(content=video.file_data, media_type="video/mp4")


@student_router.get("/lessons/{lesson_id}/pdf")
def get_pdf(lesson_id: int, db: Session = Depends(get_db_session),user: User = Depends(get_current_user)):
    pdf = db.query(Material).filter(Material.lesson_id == lesson_id, Material.type == "pdf").first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    return Response(content=pdf.file_data, media_type="application/pdf")



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
