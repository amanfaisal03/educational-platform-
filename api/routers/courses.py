"""Compose course-feature routers without containing endpoint logic."""

from fastapi import APIRouter

from api.routers.admin_courses import admin_courses_router
from api.routers.admin_materials import admin_materials_router
from api.routers.materials import materials_router
from api.routers.student_courses import student_courses_router


courses_router = APIRouter()
courses_router.include_router(admin_courses_router)
courses_router.include_router(admin_materials_router)
courses_router.include_router(student_courses_router)
courses_router.include_router(materials_router)
