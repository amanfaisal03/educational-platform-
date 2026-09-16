from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from modules.base import Base


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    course_id = Column(
        Integer,
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_active = Column(Boolean, default=True,nullable=False)

    course = relationship("Course", back_populates="units")
    lessons = relationship(
        "Lesson",
        back_populates="unit",
        cascade="all, delete-orphan",
    )

