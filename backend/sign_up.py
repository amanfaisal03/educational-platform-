from fastapi import FastAPI ,Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.schema import User , UserCourse
from typing import Literal
# from models.database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException, status ,Response
from pwdlib import PasswordHash
from passlib.context import CryptContext
from fastapi import Cookie
from models.database import get_db_session
from backend.student import get_courses_for_each_student


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

class UserCreate(BaseModel):
    name: str
    email : str
    password : str
    role: Literal["student", "admin"]


class LoginRequest(BaseModel):
    email: str
    password: str


def sign_up(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user =User (
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def sign_in(db: Session, user: LoginRequest):
    found_user = db.query(User).filter(User.email == user.email).first()

    if not found_user or not pwd_context.verify(user.password, found_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return found_user

def get_student_names(db: Session):
    students = db.query(User.id, User.name).filter(User.role == "student").all()
    return students


def add_students_to_dashboard(db: Session, student_name: str):
    students = db.query(User).filter_by(name=student_name, role="student").all()
    return students


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


def get_current_user(user_id: int = Cookie(None), db: Session = Depends(get_db_session)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Not logged in , please backend")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found , please signup ")

    return user
