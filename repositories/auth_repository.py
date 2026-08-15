
from sqlalchemy.orm import Session
from app.models import Lesson, Material, Course, Unit, UserCourse, User, user


class AuthorRepository:
    def __init__(self , db : Session):
        self.db=db

    def existing_user (self):
        return  self.db.query(User).filter(User.email == user.email).first()

    def get_student_names (self):
        return self.db.query(User.id, User.name).filter(User.role == "student").all()


__all__ = ["AuthorRepository"]
