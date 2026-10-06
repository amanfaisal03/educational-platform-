from sqlalchemy.orm import Session

from modules.courses.unit.models import Unit


class UnitRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_units_by_course_id(
        self,
        course_id: int,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Unit]:
        query = (
            self.db.query(Unit)
            .filter(Unit.course_id == course_id, Unit.is_active.is_(True))
            .order_by(Unit.id)
        )
        if limit is not None:
            query = query.offset(offset).limit(limit)
        return query.all()

    def get_unit_by_id(self, unit_id: int) -> Unit | None:
        return (
            self.db.query(Unit)
            .filter(Unit.id == unit_id, Unit.is_active.is_(True))
            .first()
        )

    def add_unit(self, course_id: int, title: str) -> Unit:
        unit = Unit(title=title, course_id=course_id)
        self.db.add(unit)
        self.db.flush()
        self.db.refresh(unit)
        return unit

    def count_units(self, course_id: int) -> int:
        return (
            self.db.query(Unit)
            .filter(
                Unit.course_id == course_id,
                Unit.is_active.is_(True),
            )
            .count()
        )


__all__ = ["UnitRepository"]
