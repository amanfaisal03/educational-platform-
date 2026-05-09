from api.admin import admin_router
from api.student import student_router
from login.sign_up import sign_up, sign_in  ,UserCreate ,LoginRequest
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from models.database import get_db_session
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


app.include_router(admin_router)
app.include_router(student_router)

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request, "sign_in.html")

@app.get("/sign_up", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse(request, "sign_up.html")

@app.post("/sign_up")
def sign_up_endpoint(name: str = Form(...),email: str = Form(...),password: str = Form(...),role: str = Form(...),db: Session = Depends(get_db_session)):
    user = UserCreate(
        name=name,
        email=email,
        password=password,
        role=role
    )
    sign_up(db, user)
    return RedirectResponse(url="/", status_code=302)



@app.post("/sign_in")
def sign_in_endpoint(email: str = Form(...),password: str = Form(...),db: Session = Depends(get_db_session)):
    user = LoginRequest(email=email, password=password)
    found_user = sign_in(db, user)

    if found_user.role == "admin":
        response = RedirectResponse(url="/admin", status_code=302)
    else:
        response = RedirectResponse(url="/student/allcourses", status_code=302)

    response.set_cookie(
        key="user_id",
        value=str(found_user.id),
        httponly=True
    )

    return response

@app.get("/signout")
def signout():
    return RedirectResponse(url="/", status_code=302)
