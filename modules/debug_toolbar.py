"""Debug toolbar integration for the application's shared database engine."""

from debug_toolbar.panels.sqlalchemy import SQLAlchemyPanel
from debug_toolbar.settings import DebugToolbarSettings
from fastapi import Request

from modules.database import engine


class ApplicationSQLAlchemyPanel(SQLAlchemyPanel):
    async def add_engines(self, request: Request) -> None:
        self.add_bind(engine)


def show_toolbar(request: Request, settings: DebugToolbarSettings) -> bool:
    return request.app.debug and request.url.hostname in (settings.ALLOWED_HOSTS or ())
