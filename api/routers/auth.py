"""

api/routers/auth.py
├── Signup
├── Sign-in
├── Sign-out
└── Current-user endpoint

"""

from services.auth_service import register_student,authenticate_user, LoginRequest , StudentRegistrationRequest
from fastapi import FastAPI, Depends, Request, Form, Response, APIRouter, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db_session
from fastapi.templating import Jinja2Templates
from app.core.security import JWT_creation, JWT_verification
from app.models.user import User

templates = Jinja2Templates(directory="templates")
auth_router = APIRouter(prefix="/api/routers/auth", tags=["Authentication"])

# @auth_router.get("/", response_class=HTMLResponse)
# def login_page(request: Request):
#     return templates.TemplateResponse(request, "login.html")

# @auth_router.get("/register", response_class=HTMLResponse)
# def signup_page(request: Request):
#     return templates.TemplateResponse(request, "register.html")



@auth_router.post("/register")
def register_student_endpoint(name: str = Form(...), email: str = Form(...), password: str = Form(...),db: Session = Depends(get_db_session)):
    user = StudentRegistrationRequest(
        name=name,
        email=email,
        password=password,
    )
    register_student(db, user)
    return RedirectResponse(url="/", status_code=302)


@auth_router.post("/login")
def login_endpoint(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db_session)):
    user = LoginRequest(email=email, password=password)
    found_user = authenticate_user(db, user)
    token = JWT_creation(
        user_id=found_user.id
    )

    response = RedirectResponse(url="/students/allcourses", status_code=302)

    response.set_cookie(
        key="authorization",
        value=f"Bearer {token}",
        httponly=True,
        secure=False,
        max_age=3600,
        path="/",
    )

    return response

@auth_router.post("/logout")
def logout_endpoint():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(
        key="authorization",
        path="/",
    )
    return response




