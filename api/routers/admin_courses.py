from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.openapi.models import Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from api.dependencies.authorization import require_admin
from api.dependencies.services import get_course_service
from services.course_service import CourseService
from services.exceptions import (
    CourseAlreadyExistsError,
    CourseNotFoundError,
    EmptyTitleError,
    LessonAlreadyExistsError,
    UnitNotFoundError,
)


admin_courses_router= APIRouter(
    prefix="/api/v1/admin",
    tags=["API v1 - AdminCourses"],
    dependencies=[Depends(require_admin)],
)
templates = Jinja2Templates(directory="templates")


@admin_courses_router.get("/courses", response_class=HTMLResponse)
def display_courses(
    request: Request,
    service: CourseService = Depends(get_course_service),
):
    return templates.TemplateResponse(
        request=request,
        name="admin/courses.html",
        context={"courses": service.list_courses()},
    )


@admin_courses_router.post("/add_courses")
def create_course(
    title: str = Form(...),
    service: CourseService = Depends(get_course_service),
):
    try:
        service.create_course(title)
    except EmptyTitleError:
        raise HTTPException(status_code=400, detail="Course title is required")
    except CourseAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Course already exists")
    return RedirectResponse("/admin/courses", status_code=status.HTTP_303_SEE_OTHER)


@admin_courses_router.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    service: CourseService = Depends(get_course_service),
):
    try:
        service.deactivate_course(course_id)
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@admin_courses_router.get("/courses/{course_id}/units", response_class=HTMLResponse)
def display_course_units(
    request: Request,
    course_id: int,
    service: CourseService = Depends(get_course_service),
):
    try:
        course = service.get_course(course_id)
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")
    return templates.TemplateResponse(
        request=request,
        name="admin/units.html",
        context={"course": course},
    )


@admin_courses_router.post("/units")
def create_course_unit(
    course_id: int = Form(...),
    title: str = Form(...),
    service: CourseService = Depends(get_course_service),
):
    try:
        service.create_unit(course_id, title)
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")
    except EmptyTitleError:
        raise HTTPException(status_code=400, detail="Unit title is required")
    return RedirectResponse(
        f"/admin/courses/{course_id}/units",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@admin_courses_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def display_unit_lessons(
    request: Request,
    unit_id: int,
    service: CourseService = Depends(get_course_service),
):
    try:
        unit = service.get_unit(unit_id)
    except UnitNotFoundError:
        raise HTTPException(status_code=404, detail="Unit not found")
    return templates.TemplateResponse(
        request=request,
        name="admin/lessons.html",
        context={"unit": unit},
    )


@admin_courses_router.post("/lessons")
def create_unit_lesson(
    unit_id: int = Form(...),
    title: str = Form(...),
    service: CourseService = Depends(get_course_service),
):
    try:
        service.create_lesson(unit_id, title)
    except UnitNotFoundError:
        raise HTTPException(status_code=404, detail="Unit not found")
    except LessonAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Lesson already exists")
    except EmptyTitleError:
        raise HTTPException(status_code=400, detail="Lesson title is required")
    return RedirectResponse(
        f"/admin/units/{unit_id}/lessons",
        status_code=status.HTTP_303_SEE_OTHER,
    )
