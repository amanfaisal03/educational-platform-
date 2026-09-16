from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from modules.base import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    unit_id = Column(
        Integer,
        ForeignKey("units.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_active = Column(Boolean, default=True,nullable=False)


    unit = relationship("Unit", back_populates="lessons")
    materials = relationship(
        "Material",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

