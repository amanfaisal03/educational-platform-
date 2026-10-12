from sqlalchemy import Boolean, Column, Enum, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from modules.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum("admin", "student", name="role_enum"), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    progress_storage = Column(String(255), nullable=False)

    courses = relationship(
        "UserCourse",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    grade_id = Column(Integer, ForeignKey("grades.id"), nullable=True)
    grade = relationship("Grade", back_populates="users")
