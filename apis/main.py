from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apis.materials import admin_router
from apis.auth import auth_router

from fastapi import APIRouter

from apis.admin_courses import admin_courses_router
from apis.admin_materials import admin_materials_router
from apis.courses import materials_router
from apis.user_course import student_courses_router

courses_router = APIRouter()
courses_router.include_router(admin_courses_router)
courses_router.include_router(admin_materials_router)
courses_router.include_router(student_courses_router)
courses_router.include_router(materials_router)

app = FastAPI(
    title="Educational Platform API",
    description="API for managing courses, students, lessons, and authentication.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)
app.include_router(courses_router)
app.include_router(admin_router)
