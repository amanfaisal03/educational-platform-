from api.admin import admin_router
from api.student import student_router
from login.sign_up import UserCreate
from fastapi.middleware.cors import CORSMiddleware
from login.sign_up import sign_up
from fastapi import FastAPI ,Depends
from sqlalchemy.orm import Session
from models.database import get_db_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(admin_router)
app.include_router(student_router)

@app.post("/sign_up")
def sing_up_endpoint(user: UserCreate, db: Session = Depends(get_db_session)):
    return sign_up(db, user)
