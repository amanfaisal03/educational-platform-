from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from api.dependencies.authorization import require_admin
from app.db.database import get_db_session
from services.auth_service import delete_student, get_student_names


admin_router = APIRouter(prefix="/admin",tags=["Admin"],dependencies=[Depends(require_admin)],)
templates = Jinja2Templates(directory="templates")


@admin_router.get("", response_class=HTMLResponse)
@admin_router.get("/", response_class=HTMLResponse, include_in_schema=False)
def admin_page(request: Request, db: Session = Depends(get_db_session)):
    return templates.TemplateResponse(
        request=request,
        name="admin/admin_core_page.html",
        context={"students": get_student_names(db)},
    )


@admin_router.post("/students/delete")
def delete_student(
    student_id: int = Form(...),
    db: Session = Depends(get_db_session),
):
    if not delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)
