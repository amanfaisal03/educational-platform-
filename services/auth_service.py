"""
services/auth_service.py
├── register_student
└── authenticate_user

"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_course import UserCourse
from fastapi import  HTTPException
from app.schemas.auth import LoginRequest,StudentRegistrationRequest
from services.student_service import get_courses_for_each_student
from app.core.security import JWT_creation, JWT_verification, hash_password, verify_password
from repositories.auth_repository import AuthorRepository


def register_student(db: Session, user: StudentRegistrationRequest):
    if AuthorRepository.existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        name=user.name,
        email=user.email.lower().strip(),
        password=hash_password(user.password),
        role="student",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user( user: LoginRequest):
    if not AuthorRepository.existing_user or not verify_password(user.password, found_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return found_user

def get_student_names(db: Session):
    return AuthorRepository.get_student_names


# def add_students_to_dashboard(db: Session, student_name: str):
#     existing = db.query(User).filter_by(name=student_name, role="student").first()
#     if existing:
#         return None
#
#     new_student = User(name=student_name, role="student")
#     db.add(new_student)
#     db.commit()
#     db.refresh(new_student)
#     return new_student


def delete_student(db: Session, student_id: int):
    student = db.query(User).filter_by(id=student_id, role="student").first()
    if not student:
        return False

    courses = get_courses_for_each_student(student_id, db)
    if courses:
        db.query(UserCourse).filter(UserCourse.user_id == student_id).delete()
        db.flush()

    db.delete(student)
    db.commit()
    return True

 # cant delete student , i have course related with student so i need to delete corses for this student too.


