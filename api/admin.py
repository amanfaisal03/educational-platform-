from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File ,Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from models.database import get_db_session
from models.schema import Material
from backend.sign_up import get_student_names, delete_student ,get_current_user
from backend.admin import add_course_to_dashbord,delete_course_from_dashboard,add_unite_to_course,add_lesson_by_unite ,upload_material
from fastapi.templating import Jinja2Templates
from backend.student import get_courses_from_dashboard, get_unite_by_course_id, get_lesson_by_unit_id
from models.schema import Course, Unit, Lesson ,User


admin_router = APIRouter(prefix="/admin",dependencies=[Depends(get_current_user)])
templates = Jinja2Templates(directory="templates")

@admin_router.get("/", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db_session)):
    students = get_student_names(db)
    return templates.TemplateResponse(request, "admin/admin_core_page.html", {"students": students})

@admin_router.get("/students", response_class=HTMLResponse)
def get_students(request: Request, db: Session = Depends(get_db_session)):
    students = get_student_names(db)
    return templates.TemplateResponse(request, "admin/admin_core_page.html", {"students": students})


# @admin_router.post("/students")
# def add_students_endpoint(student_name: str = Form(...),db: Session = Depends(get_db_session)):
#     student = add_students_to_dashboard(db, student_name)
#     if student:
#         return {"message": "Student added successfully"}
#     else:
#         return {"message": "Student not found in database"}

@admin_router.post("/students/delete")
def delete_student_endpoint(student_id: int = Form(...), db: Session = Depends(get_db_session)):
    success = delete_student(db, student_id)
    if success:
        return {"message": "Student deleted successfully"}
    else:
        return {"message": "Student not found"}



@admin_router.get("/courses", response_class=HTMLResponse)
def get_courses_page(request: Request, db: Session = Depends(get_db_session)):
    courses = get_courses_from_dashboard(db)
    return templates.TemplateResponse(request,
                                      "/admin/courses.html",
                                      {"courses": courses})


@admin_router.post("/add_courses")
def add_course_endpoint(title: str = Form(...),db: Session = Depends(get_db_session)):
    new_course = add_course_to_dashbord(title, db)
    return RedirectResponse(url="/admin/courses", status_code=303)


@admin_router.post("/courses/{course_id}") # i want to handel it in html page
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db_session)):
    success = delete_course_from_dashboard(course_id, db)
    if success:
        return {"message": "Course deleted successfully"}
    else:
        return {"message": "Course not found"}


@admin_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def get_units_for_course(request: Request,course_id: int,db: Session = Depends(get_db_session)):
    course = db.query(Course).filter(Course.id == course_id).first()   ##### askkkkk

    return templates.TemplateResponse(request,
        "admin/units.html",
        {
            "course": course
        }
    )


@admin_router.post("/units")
def add_unit_to_course_endpoint(course_id: int = Form(...),title: str = Form(...),db: Session = Depends(get_db_session)):
    unit = add_unite_to_course(course_id, title, db)
    return RedirectResponse(url=f"/admin/courses/{course_id}/units", status_code=303)



@admin_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def get_lessons_for_unit(request: Request,unit_id: int,db: Session = Depends(get_db_session)):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()

    return templates.TemplateResponse(
        request=request,
        name="admin/lessons.html",
        context={
            "unit": unit,
        }
    )


@admin_router.post("/lessons")
def add_lesson_to_unit_endpoint(unit_id: int = Form(...),title: str = Form(...),db: Session = Depends(get_db_session)):
    lesson = add_lesson_by_unite(unit_id, title, db)
    return RedirectResponse(url=f"/admin/units/{unit_id}/lessons", status_code=303)



@admin_router.post("/lessons/upload-video")
def upload_video(lesson_id: int = Form(...),file: UploadFile = File(...),db: Session = Depends(get_db_session)):
    return upload_material(lesson_id, file, "video", db)

@admin_router.post("/lessons/upload-pdf")
def upload_video(lesson_id: int = Form(...),file: UploadFile = File(...),db: Session = Depends(get_db_session)):
    return upload_material(lesson_id, file, "pdf", db)

#
# # @app.delete("/unit/{unit_id}")
# # def delete_unit_from_course_endpoint(unit_id: int, db: Session = Depends(get_db_session)):
# #     result = delete_unit_from_course(unit_id, db)
# #     return {"message": "Unit deleted from the course successfully"}
#
# """
# ask ahamd how can delete unit from course :
# i cant delete unit directly because the unit is linked to the lessons
# """
