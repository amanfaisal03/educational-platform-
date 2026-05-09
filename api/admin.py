from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File ,Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from models.database import get_db_session
from models.schema import Material
from login.sign_up import get_student_names, delete_student, add_students_to_dashboard ,sign_up
from login.admin import add_course_to_dashbord,delete_course_from_dashboard,add_unite_to_course,add_lesson_by_unite
from fastapi.templating import Jinja2Templates

admin_router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")


@admin_router.get("/", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db_session)):
    students = get_student_names(db)
    return templates.TemplateResponse(request, "admin.html", {"students": students})

@admin_router.get("/students", response_class=HTMLResponse)
def get_students(request: Request, db: Session = Depends(get_db_session)):
    students = get_student_names(db)
    return templates.TemplateResponse(request, "admin.html", {"students": students})



@admin_router.post("/students")
def add_students_endpoint(student_name: str = Form(...),db: Session = Depends(get_db_session)):
    add = add_students_to_dashboard(db, student_name)
    if add:
        return {"message": "Student added successfully"}
    else:
        return {"message": "Student not found in database"}


@admin_router.post("/students/{student_id}")
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db_session)):
    success = delete_student(db, student_id)
    if success:
        return {"message": "Student deleted successfully"}
    else:
        return {"message": "Student not found"}


@admin_router.post("/add_courses")
def add_course_endpoint(title: str = Form(...),db: Session = Depends(get_db_session)):

    new_course = add_course_to_dashbord(title, db)
    if new_course:
        return {"message": "Course added successfully"}
    else:
        return {"message": "Course already exists"}


@admin_router.post("/courses/{course_id}")
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db_session)):
    success = delete_course_from_dashboard(course_id, db)
    if success:
        return {"message": "Course deleted successfully"}
    else:
        return {"message": "Course not found"}



@admin_router.post("/units")
def add_unit_to_course_endpoint(course_id: int = Form(...),title: str = Form(...),db: Session = Depends(get_db_session)):
    unit = add_unite_to_course(course_id, title, db)
    if unit:
        return {"message": "Unit added successfully"}
    else:
        return {"message": "Unit already exists"}


@admin_router.post("/lessons")
def add_lesson_to_unit_endpoint(unit_id: int = Form(...),title: str = Form(...),db: Session = Depends(get_db_session)):
    lesson = add_lesson_by_unite(unit_id, title, db)
    if lesson:
        return {"message": "Lesson added successfully"}
    else:
        return {"message": "Lesson already exists"}


@admin_router.post("/lessons/{lesson_id}/upload-video")
def upload_video(lesson_id: int,file: UploadFile = File(...),db: Session = Depends(get_db_session)):
    existing = db.query(Material).filter(Material.lesson_id == lesson_id,Material.type == "video").first()
    if existing:
        return {"message": "Video already exists for this lesson"}

    file_data = file.file.read()
    material = Material(
        lesson_id=lesson_id,
        type="video",
        file_data=file_data
    )

    db.add(material)
    db.commit()
    db.refresh(material)

    return {
        "message": "Video uploaded successfully",
        "material_id": material.id
    }


@admin_router.post("/lessons/{lesson_id}/upload-pdf")
def upload_pdf(lesson_id: int,file: UploadFile = File(...),db: Session = Depends(get_db_session)):
    existing = db.query(Material).filter( Material.lesson_id == lesson_id,Material.type == "pdf").first()

    if existing:
        return {"message": "PDF already exists for this lesson"}

    file_data = file.file.read()

    material = Material(
        lesson_id=lesson_id,
        type="pdf",
        file_data=file_data
    )

    db.add(material)
    db.commit()
    db.refresh(material)

    return {
        "message": "PDF uploaded successfully",
        "material_id": material.id
    }

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
