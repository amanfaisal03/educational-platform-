from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from debug_toolbar.middleware import DebugToolbarMiddleware

from apis.materials import admin_router
from apis.auth import auth_router
from modules.Config import settings

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
    debug=settings.debug_toolbar_enabled,
)


def configure_debug_toolbar(app: FastAPI) -> None:
    if not settings.debug_toolbar_enabled:
        return

    app.add_middleware(
        DebugToolbarMiddleware,
        ALLOWED_HOSTS=None,
        PANELS=[
            "debug_toolbar.panels.versions.VersionsPanel",
            "debug_toolbar.panels.timer.TimerPanel",
            "debug_toolbar.panels.settings.SettingsPanel",
            "debug_toolbar.panels.request.RequestPanel",
            "debug_toolbar.panels.headers.HeadersPanel",
            "debug_toolbar.panels.routes.RoutesPanel",
            "debug_toolbar.panels.logging.LoggingPanel",
            "debug_toolbar.panels.redirects.RedirectsPanel",
            "debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel",
        ],
    )


configure_debug_toolbar(app)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)
app.include_router(courses_router)
app.include_router(admin_router)


@app.get("/api/v1/debug-toolbar/status", tags=["API v1 - Debug"])
def debug_toolbar_status() -> dict:
    return {
        "enabled": settings.debug_toolbar_enabled,
        "api_url": "/_debug_toolbar",
        "static_url": "/_debug_toolbar/static",
        "allowed_hosts": settings.debug_toolbar_allowed_hosts,
        "proxy_ready": True,
        "profiling_panel": "disabled",
    }
