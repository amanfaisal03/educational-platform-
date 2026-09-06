from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers.admin import admin_router
from api.routers.auth import auth_router
from api.routers.courses import courses_router


app = FastAPI(
    title="Educational Platform API",
    description="API for managing courses, students, lessons, and authentication.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)
app.include_router(courses_router)
app.include_router(admin_router)
