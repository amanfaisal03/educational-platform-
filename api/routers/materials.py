from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from api.dependencies.authorization import require_student
from app.db.database import get_db_session
from app.models import Material


materials_router = APIRouter(
    prefix="/student/lessons",
    tags=["Materials"],
    dependencies=[Depends(require_student)],
)


def _get_material(lesson_id: int, material_type: str, db: Session) -> Response:
    material = db.query(Material).filter(
        Material.lesson_id == lesson_id,
        Material.type == material_type,
    ).first()
    if material is None or material.file_data is None:
        raise HTTPException(status_code=404, detail=f"{material_type.title()} not found")
    content_types = {"video": "video/mp4", "pdf": "application/pdf"}
    return Response(material.file_data, media_type=content_types[material_type])


@materials_router.get("/{lesson_id}/video")
def get_video(lesson_id: int, db: Session = Depends(get_db_session)):
    return _get_material(lesson_id, "video", db)


@materials_router.get("/{lesson_id}/pdf")
def get_pdf(lesson_id: int, db: Session = Depends(get_db_session)):
    return _get_material(lesson_id, "pdf", db)
