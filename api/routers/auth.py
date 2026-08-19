from fastapi import APIRouter, Depends, Form, Request, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from api.dependencies.services import get_auth_service, get_token_service
from app.schemas.auth import LoginRequest, StudentRegistrationRequest
from services.auth_service import AuthService
from services.exceptions import UserAlreadyExistsError, InvalidCredentialsError
from services.token_service import TokenService

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["API V1 - Authentication"])
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
    service:AuthService = Depends(get_auth_service),
):
    request=StudentRegistrationRequest(
        name=name,
        email=email,
        password=password,
    )
    try:
        service.register_student(request)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )

    return RedirectResponse(
        "/sign_in",
        status_code=303,
    )


@auth_router.post("/sign_in")
def login(
    email: str = Form(...),
    password: str = Form(...),
    service:AuthService = Depends(get_auth_service),
    token_service: TokenService = Depends(get_token_service),
):
    try :
        user=service.authenticate(
            LoginRequest(email=email,
                         password=password)
        )
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = token_service.create_access_token(user.id)
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
