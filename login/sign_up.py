from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.schema import User
from typing import Literal
# from models.database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException, status
from pwdlib import PasswordHash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserCreate(BaseModel):
    name: str
    email : str
    password : str
    role: Literal["student", "admin"]


def sign_up(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_student_names(db: Session):
    students = db.query(User.id, User.name).filter(User.role == "student").all()
    return students


def add_students_to_dashboard(db: Session, student_name: str):
    students = db.query(User).filter_by(name=student_name, role="student").all()
    return students


def delete_student(db: Session, student_id: int):
    student = db.query(User).filter_by(id=student_id, role="student").first()
    if student:
        db.delete(student)
        db.commit()
        return True
    return False


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return False
    if not PasswordHash.verify(password, user.password):
        return False
    return user



