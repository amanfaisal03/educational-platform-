from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from api.dependencies.authorization import require_student
from api.dependencies.services import get_material_service
from services.exceptions import LessonNotFoundError
from services.material_service import MaterialService


materials_router = APIRouter(
    prefix="/api/v1/student/lessons",
    tags=["API V1 - Materials"],
    dependencies=[Depends(require_student)],
)


def _get_material(
    lesson_id: int,
    material_type: str,
    service: MaterialService,
) -> Response:
    try:
        material = service.get_material(lesson_id, material_type)
    except LessonNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"{material_type.title()} not found",
        )

    content_types = {"video": "video/mp4", "pdf": "application/pdf"}
    return Response(
        material.file_data,
        media_type=content_types[material_type],
    )


@materials_router.get("/{lesson_id}/video")
def get_video(
    lesson_id: int,
    service: MaterialService = Depends(get_material_service),
):
    return _get_material(lesson_id, "video", service)


@materials_router.get("/{lesson_id}/pdf")
def get_pdf(
    lesson_id: int,
    service: MaterialService = Depends(get_material_service),
):
    return _get_material(lesson_id, "pdf", service)
