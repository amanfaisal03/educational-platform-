from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.auth.authorization import require_admin
from modules.exceptions import StudentNotFoundError
from modules.users.service import StudentAdminService, get_student_admin_service

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["API v1 - Admin"],
    dependencies=[Depends(require_admin)],
)
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def admin_page(
    request: Request,
    service: StudentAdminService = Depends(get_student_admin_service),
):
    students = service.list_students()
    return templates.TemplateResponse(
        request=request,
        name="admin/admin_core_page.html",
        context={"students": students},
    )


@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    service: StudentAdminService = Depends(get_student_admin_service),
) -> Response:
    try:
        service.delete_student(student_id)
    except StudentNotFoundError:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/students/delete", status_code=status.HTTP_303_SEE_OTHER)
def delete_student_from_form(
    student_id: int = Form(...),
    service: StudentAdminService = Depends(get_student_admin_service),
):
    try:
        service.delete_student(student_id)
    except StudentNotFoundError:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(
        status_code=status.HTTP_303_SEE_OTHER,
        headers={"Location": "/api/v1/admin"},
    )
