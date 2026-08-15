from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db_session
from repositories.material_repository import MaterialRepository
from services.material_service import MaterialService


def get_material_service(db: Session = Depends(get_db_session),) -> MaterialService:
    return MaterialService(MaterialRepository(db))
