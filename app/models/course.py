from sqlalchemy import Column, String, Integer, ForeignKey, Enum, LargeBinary
from sqlalchemy.orm import relationship

from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    units = relationship("Unit", back_populates="course")
    users = relationship("UserCourse", back_populates="course")

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", back_populates="units")
    lessons = relationship("Lesson", back_populates="unit")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    unite_id = Column(Integer, ForeignKey("units.id"), nullable=False)

    unit = relationship("Unit", back_populates="lessons")
    materials = relationship("Material", back_populates="lesson")


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum("pdf", "video", name="material_type_enum"), nullable=False)

    file_data = Column(LargeBinary, nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)

    lesson = relationship("Lesson", back_populates="materials")


