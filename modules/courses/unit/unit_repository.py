from modules.courses.unit.models import Unit
from sqlalchemy.orm import Session

class UnitRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_units_by_course_id(self, course_id: int) -> list[Unit]:
        return self.db.query(Unit).filter(Unit.course_id == course_id,Unit.is_active.is_(True)).all()

    def get_unit_by_id(self, unit_id: int) -> Unit | None:
        return self.db.query(Unit).filter(Unit.id == unit_id).first()

    def add_unit(self, course_id: int, title: str) -> Unit:
        unit = Unit(title=title, course_id=course_id)
        self.db.add(unit)
        self.db.flush()
        self.db.refresh(unit)
        return unit

__all__ = ["UnitRepository"]
