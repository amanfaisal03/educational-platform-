from fastapi import FastAPI

from api.routers.admin import admin_router
from api.routers.auth import auth_router
from api.routers.courses import courses_router
from api.routers.student import student_router


app = FastAPI(
    title="Educational Platform API",
    description="API for managing courses, students, lessons, and authentication.",
    version="1.0.0",
)
app.include_router(auth_router)
app.include_router(courses_router)
app.include_router(student_router)
app.include_router(admin_router)

@app.get("/", tags=["General"])
def root():
    return {"message": "Educational Platform API is running"}