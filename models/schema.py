from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import LargeBinary

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("admin", "student", name="role_enum"), nullable=False)


    courses = relationship("UserCourse", back_populates="user")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    units = relationship("Unit", back_populates="course")
    users = relationship("UserCourse", back_populates="course")


class UserCourse(Base):
    __tablename__ = "user_courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    user = relationship("User", back_populates="courses")
    course = relationship("Course", back_populates="users")


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

__all__ = [
    "Base",
    "User",
    "Course",
    "UserCourse",
    "Unit",
    "Lesson",
    "Material",
]
