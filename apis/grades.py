from typing import List

from fastapi import APIRouter, Depends , Form, HTTPException
from modules.auth.authorization import require_admin
from modules.auth.services import get_grade_service
from modules.exceptions import EmptyTitleError, GradeAlreadyExistsError
from modules.grade.grade_service import GradeService
from modules.grade.models import Grade
from starlette import status
from starlette.responses import RedirectResponse

admin_courses_router= APIRouter(
    prefix="/api/v1/admin",
    tags=["API v1 - Grades"],
    dependencies=[Depends(require_admin)],
)

@admin_courses_router.post("/add_grade")
def create_grade(
    name: str = Form(...),
    servics:GradeService=Depends(get_grade_service),):

    try:
        servics.create_grade(name)
    except EmptyTitleError:
        raise HTTPException(status_code=400, detail="Grade is required")
    except GradeAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Grade already exists")
    return RedirectResponse("/api/v1/admin/courses", status_code=status.HTTP_303_SEE_OTHER)

