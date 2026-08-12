from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File ,Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db.database import get_db_session
from services.auth_service import get_student_names, delete_student
from services.admin_service import add_unite_to_course,add_lesson_by_unite ,upload_material
from fastapi.templating import Jinja2Templates
from api.dependencies.authorization import require_admin


admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],)


templates = Jinja2Templates(directory="templates")

@admin_router.get("/", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db_session)):
    students = get_student_names(db)
    return templates.TemplateResponse(request, "admin/admin_core_page.html", {"students": students})


@admin_router.post("/students/delete")
def delete_student_endpoint(student_id: int = Form(...), db: Session = Depends(get_db_session)):
    success = delete_student(db, student_id)
    if success:
        return {"message": "Student deleted successfully"}
    else:
        return {"message": "Student not found"}

@admin_router.post("/units")
def add_unit_to_course_endpoint(course_id: int = Form(...),title: str = Form(...),db: Session = Depends(get_db_session)):
    unit = add_unite_to_course(course_id, title, db)
    return RedirectResponse(url=f"/admin/courses/{course_id}/units", status_code=303)

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