"""Compose course-feature routers without containing endpoint logic."""

from fastapi import APIRouter

from api.routers.admin_courses import admin_courses_router
from api.routers.materials import materials_router
from api.routers.student_courses import student_courses_router


app = APIRouter()
app.include_router(admin_courses_router)
app.include_router(student_courses_router)
app.include_router(materials_router)
