from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from api.dependencies.authorization import require_admin
from api.dependencies.services import get_student_admin_service
from services.exceptions import StudentNotFoundError
from services.student_admin_services import StudentAdminService

admin_router = APIRouter(prefix="/api/v1/admin",tags=["API v1 - Admin"],dependencies=[Depends(require_admin)],)
templates = Jinja2Templates(directory="templates")


@admin_router.get("", response_class=HTMLResponse)
@admin_router.get("/", response_class=HTMLResponse, include_in_schema=False)
def admin_page(request: Request, service:StudentAdminService = Depends(get_student_admin_service)):
    students=service.list_students()

    return templates.TemplateResponse(
        request=request,
        name="admin/admin_core_page.html",
        context={"students": students},
    )

@admin_router.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: int,
    service: StudentAdminService = Depends(get_student_admin_service),
) -> Response:
    try:
        service.delete_student(student_id)
    except StudentNotFoundError:
        raise HTTPException(status_code=404, detail="Student not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
