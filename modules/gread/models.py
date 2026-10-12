from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from modules.base import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    users = relationship("User", back_populates="grade")
    courses = relationship("Course", back_populates="grade")