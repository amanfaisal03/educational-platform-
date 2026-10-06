from fastapi import APIRouter, Depends, HTTPException, Response, status, Form, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from modules.auth.authorization import require_admin
from modules.auth.services import (
    get_course_service,
    get_lesson_service,
    get_unit_service,
)
from modules.courses.course.service import  CourseService
from modules.courses.lesson.service import LessonService
from modules.courses.unit.service import UnitService
from modules.exceptions import (
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
    page: int = Query(1, ge=1),
    service: CourseService = Depends(get_course_service),
):
    per_page = 6
    courses, page, total_pages = service.list_courses_paginated(page, per_page)

    return templates.TemplateResponse(
        request=request,
        name="admin/courses.html",
        context={
            "courses": courses,
            "page": page,
            "total_pages": total_pages,
        },
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
    return RedirectResponse("/api/v1/admin/courses", status_code=status.HTTP_303_SEE_OTHER)


@admin_courses_router.post("/courses/{course_id}")
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



@admin_courses_router.post("/units")
def create_course_unit(
    course_id: int = Form(...),
    title: str = Form(...),
    service: UnitService = Depends(get_unit_service),
):
    try:
        service.create_unit(course_id, title)
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")
    except EmptyTitleError:
        raise HTTPException(status_code=400, detail="Unit title is required")
    return RedirectResponse(
        f"/api/v1/admin/courses/{course_id}/units",
        status_code=status.HTTP_303_SEE_OTHER,
    )

@admin_courses_router.get("/courses/{course_id}/units")
def display_units(
    request: Request,
    course_id: int,
    service: UnitService = Depends(get_unit_service),
    page: int = Query(1, ge=1),
    course: CourseService = Depends(get_course_service),

):
    try:
        course = course.get_course(course_id)
        per_page = 6
        units, page, total_pages = service.get_units_by_course_id_paginated(
            course_id,
            page,
            per_page,
        )
    except UnitNotFoundError:
        raise HTTPException(status_code=404, detail="Unit not found")
    except CourseNotFoundError:
        raise HTTPException(status_code=404, detail="Course not found")

    return templates.TemplateResponse(
        request=request,
        name="/admin/units.html",
        context={
            "course": course,
            "units": units,
            "page": page,
            "total_pages": total_pages,
        },
    )


@admin_courses_router.post("/lessons")
def create_unit_lesson(
    unit_id: int = Form(...),
    title: str = Form(...),
    service: LessonService = Depends(get_lesson_service),
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
        f"/api/v1/admin/units/{unit_id}/lessons",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@admin_courses_router.get("/units/{unit_id}/lessons", response_class=HTMLResponse)
def display_admin_unit_lessons(
    request: Request,
    unit_id: int,
    service: LessonService = Depends(get_lesson_service),
    page: int = Query(1, ge=1),
):

    per_page = 6
    try:
        unit = service.get_unit(unit_id)
        lessons, page, total_pages = service.get_lessons_by_unit_id_paginated(
            unit_id,
            page,
            per_page,
        )
    except UnitNotFoundError:
        raise HTTPException(status_code=404, detail="Unit not found")

    return templates.TemplateResponse(
        request=request,
        name="admin/lessons.html",
        context={
            "unit": unit,
            "lessons": lessons,
            "page": page,
            "total_pages": total_pages,
            "per_page": per_page,
        },
    )
