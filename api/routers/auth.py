from typing import Optional

from api.routers.admin import admin_router
from api.routers.student import student_router
from services.auth_service import sign_up, sign_in, UserCreate, LoginRequest
from fastapi import FastAPI, Depends, Request, Form, Response, APIRouter, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db_session
from fastapi.templating import Jinja2Templates
from services.auth_service import get_current_user
from app.core.security import create_access_token, verify_token
from app.db.schema import User
from sqlalchemy import text


templates = Jinja2Templates(directory="templates")
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
@auth_router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "sign_in.html")


@auth_router.get("/sign_up", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse(request, "sign_up.html")


@auth_router.post("/sign_up")
def sign_up_endpoint(name: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(...),
                     db: Session = Depends(get_db_session)):
    user = UserCreate(
        name=name,
        email=email,
        password=password,
        role=role
    )
    sign_up(db, user)
    return RedirectResponse(url="/", status_code=302)

@auth_router.post("/sign_in")
def sign_in_endpoint(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db_session)):
    user = LoginRequest(email=email, password=password)
    found_user = sign_in(db, user)

    token = create_access_token(
        email=found_user.email,
        user_id=found_user.id,
        role=found_user.role
    )

    if found_user.role == "admin":
        response = RedirectResponse(url="/admin", status_code=302)
    else:
        response = RedirectResponse(url="/student/allcourses", status_code=302)

    response.set_cookie(
        key="authorization",
        value=f"Bearer {token}",
        httponly=True,
        secure=True,
        max_age=86400
    )

    return response

@auth_router.get("/signout")
def signout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(
        key="authorization",
    )
    return response

@auth_router.get("/auth/me")
def get_current_user(authorization: Optional[str] = Cookie(None), db: Session = Depends(get_db_session)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not logged in, please sign in")

    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token format")

        token = authorization.replace("Bearer ", "")
        token_data = verify_token(token)

        user = db.query(User).filter(User.id == token_data.user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


