from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import RedirectResponse

from api.dependencies.authorization import require_admin
from api.dependencies.services import get_material_service
from services.exceptions import (
    EmptyMaterialError,
    InvalidMaterialTypeError,
    LessonNotFoundError,
)
from services.material_service import MaterialService


admin_materials_router = APIRouter(
    prefix="/api/v1/admin/lessons",
    tags=["API V1 - Admin materials"],
    dependencies=[Depends(require_admin)],
)


async def _upload(
    lesson_id: int,
    file: UploadFile,
    material_type: str,
    service: MaterialService,
):
    file_data = await file.read()
    try:
        result = service.create_material(lesson_id, material_type, file_data)
    except LessonNotFoundError:
        raise HTTPException(status_code=404, detail="Lesson not found")
    except InvalidMaterialTypeError:
        raise HTTPException(status_code=400, detail="Invalid material type")
    except EmptyMaterialError:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    return RedirectResponse(
        f"/admin/units/{result.unit_id}/lessons",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@admin_materials_router.post("/upload-video")
async def upload_video(
    lesson_id: int = Form(...),
    file: UploadFile = File(...),
    service: MaterialService = Depends(get_material_service),
):
    return await _upload(lesson_id, file, "video", service)


@admin_materials_router.post("/upload-pdf")
async def upload_pdf(
    lesson_id: int = Form(...),
    file: UploadFile = File(...),
    service: MaterialService = Depends(get_material_service),
):
    return await _upload(lesson_id, file, "pdf", service)
