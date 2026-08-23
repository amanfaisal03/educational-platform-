from sqlalchemy import Column, Enum, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum("admin", "student", name="role_enum"), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    courses = relationship(
        "UserCourse",
        back_populates="user",
        cascade="all, delete-orphan",
    )


