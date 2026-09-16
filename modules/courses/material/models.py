from sqlalchemy import Column, Enum, ForeignKey, Integer, LargeBinary, Boolean
from sqlalchemy.orm import relationship

from modules.base import Base


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
