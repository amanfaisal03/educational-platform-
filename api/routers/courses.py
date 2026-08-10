from urllib.request import Request

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, Response

from api.routers.auth import get_current_user, templates
from app.db.database import get_db_session
from app.db.schema import Course, Unit, Material
from services.admin_service import delete_course_from_dashboard
from services.student_service import get_courses_from_dashboard, get_unite_by_course_id, get_lesson_by_unit_id

courses_router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
    dependencies=[Depends(get_current_user)],
)

@courses_router.get("/courses", response_class=HTMLResponse)
def get_courses_page(request: Request, db: Session = Depends(get_db_session)):
    courses = get_courses_from_dashboard(db)
    return templates.TemplateResponse(request,
                                      "/admin/courses.html",
                                      {"courses": courses})


@courses_router.post("/courses/{course_id}")
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db_session)):
    success = delete_course_from_dashboard(course_id, db)
    if success:
        return {"message": "Course deleted successfully"}
    else:
        return {"message": "Course not found"}


@courses_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def get_units_for_course(request: Request,course_id: int,db: Session = Depends(get_db_session)):
    course = db.query(Course).filter(Course.id == course_id).first()

    return templates.TemplateResponse(request,
        "admin/units.html",
        {
            "course": course
        }
    )


@courses_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def get_units_page(request: Request, course_id: int, db: Session = Depends(get_db_session)):
    course= get_unite_by_course_id(course_id, db)
    return templates.TemplateResponse(request, "student/units.html",  {"course": course})


@courses_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def get_lessons_for_unit(request: Request,unit_id: int,db: Session = Depends(get_db_session)):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    # remove unite query to function
    return templates.TemplateResponse(
        request=request,
        name="admin/lessons.html",
        context={
            "unit": unit,
        }
    )

@courses_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def get_lessons_page(request: Request, unit_id: int, db: Session = Depends(get_db_session)):
    unite = get_lesson_by_unit_id(unit_id, db)
    return templates.TemplateResponse(request, "student/lessons.html", {"unite": unite})


@courses_router.get("/lessons/{lesson_id}/video")
def get_video(lesson_id: int, db: Session = Depends(get_db_session)):
    video = db.query(Material).filter(Material.lesson_id == lesson_id, Material.type == "video").first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return Response(content=video.file_data, media_type="video/mp4")


@courses_router.get("/lessons/{lesson_id}/pdf")
def get_pdf(lesson_id: int, db: Session = Depends(get_db_session)):
    pdf = db.query(Material).filter(Material.lesson_id == lesson_id, Material.type == "pdf").first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")
    return Response(content=pdf.file_data, media_type="application/pdf")