from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from modules.base import Base
from modules.gread.models import Grade


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True,nullable=False)

    units = relationship(
        "Unit",
        back_populates="course",
        cascade="all, delete-orphan",
    )
    users = relationship(
        "UserCourse",
        back_populates="course",
        cascade="all, delete-orphan",
    )
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=False)
    grade = relationship("Grade", back_populates="courses")
