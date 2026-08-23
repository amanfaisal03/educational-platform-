from sqlalchemy import Column, Enum, ForeignKey, Integer, LargeBinary, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


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


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    unite_id = Column(
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


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("pdf", "video", name="material_type_enum"), nullable=False)
    file_data = Column(LargeBinary, nullable=True)
    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_active = Column(Boolean, default=True,nullable=False)
    lesson = relationship("Lesson", back_populates="materials")
