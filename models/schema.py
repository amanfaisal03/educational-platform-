from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.orm import Session


Base = declarative_base()
engine = create_engine('postgresql://platform_user:platform_password@localhost:5433/platformdb')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    role = Column(String)

    # def __repr__(self):
    #     return f"<User(name={self.name}, email={self.email}, role={self.role})>"

class UserCourse(Base):
    __tablename__ = 'user_courses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    units = relationship("Unit", back_populates="course")


class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    course_id = Column(Integer, ForeignKey('courses.id'))

    course = relationship("Course", back_populates="units")
    lessons = relationship("Lesson", back_populates="unit")


class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    unit_id = Column(Integer, ForeignKey('units.id'))

    unit = relationship("Unit", back_populates="lessons")
    materials = relationship("Material", back_populates="lesson")


class Material(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    file_url = Column(String)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))

    lesson = relationship("Lesson", back_populates="materials")

    def create_material(self):
        pass

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


###delete this file ---- > just for study orm