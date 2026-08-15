from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.security import JWT_creation
from app.db.database import get_db_session
from app.schemas.auth import LoginRequest, StudentRegistrationRequest
from services.auth_service import authenticate_user, register_student


auth_router = APIRouter(tags=["Authentication"])
templates = Jinja2Templates(directory="templates")


@auth_router.get("/", response_class=HTMLResponse)
@auth_router.get("/sign_in", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})


@auth_router.get("/sign_up", response_class=HTMLResponse)
def registration_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={})


@auth_router.post("/auth/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db_session),
):
    register_student(db, StudentRegistrationRequest(name=name, email=email, password=password))
    return RedirectResponse("/sign_in", status_code=status.HTTP_303_SEE_OTHER)


@auth_router.post("/sign_in")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db_session),
):
    user = authenticate_user(db, LoginRequest(email=email, password=password))
    token = JWT_creation(user.id)
    destination = "/admin" if user.role == "admin" else "/student/allcourses"
    response = RedirectResponse(destination, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        "authorization",
        f"Bearer {token}",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600,
        path="/",
    )
    return response


@auth_router.get("/signout", include_in_schema=False)
@auth_router.post("/signout")
def logout():
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("authorization", path="/")
    return response
