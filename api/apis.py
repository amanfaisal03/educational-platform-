from starlette.responses import Response
from login.sign_up import sign_up, UserCreate, get_student_names,delete_student , add_students_to_dashboard
from fastapi.middleware.cors import CORSMiddleware
from login.sign_up import sign_up
from login.admin import add_course_to_dashbord, delete_course_from_dashboard , add_unite_to_course , add_lesson_to_dashbord
from login.student import get_courses_from_dashboard ,get_unite_by_course_id , get_lesson_by_unit_id
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, UploadFile, File, Depends ,APIRouter
from sqlalchemy.orm import Session
from models.database import get_db_session
from models.schema import Material

app= FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allpw_origins=[settings.front_end_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
@app.post("/sign_up")
def sing_up_endpoint(user: UserCreate, db: Session = Depends(get_db_session)):
    return sign_up(db, user)


@router.get("/Admin/students")
def get_students(db: Session = Depends(get_db_session)):
    students = get_student_names(db)
    result = []
    for student in students:
        result.append({
            "id": student.id,
            "name": student.name
        })

    return result


@router.post("/Admin/students/{student_name}")
def add_students_endpoint(student_name=str, db: Session = Depends(get_db_session)):
    add= add_students_to_dashboard(db, student_name)
    if add :
       return {"message": "Students added successfully"}
    else:
        return {"message": "Student not found in the database"}

@router.delete("/Admin/students/{student_id}")
def delete_student_endpoint(student_id: int, db: Session = Depends(get_db_session)):
    success = delete_student(db, student_id)
    if success:
        return {"message": "Student deleted successfully"}
    else:
        return {"message": "Student not found"}


@router.post("/Admin/add_course")
def add_course_endpoint(title:str, db: Session = Depends(get_db_session)):
    new_course = add_course_to_dashbord(title, db)
    if new_course:
        return {"message": "Course added successfully"}
    else:
        return {"message": "Course already exists in the dashboard"}


@router.get("/Student/get_courses")
def get_courses_endpoint(db: Session = Depends(get_db_session)):
    courses = get_courses_from_dashboard(db)
    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "title": course.title
        })
    return result

@router.delete("/Admin/courses/{course_id}")
def delete_course_endpoint(course_id: int, db: Session = Depends(get_db_session)):
    success = delete_course_from_dashboard(course_id, db)
    if success:
        return {"message": "Course deleted successfully"}
    else:
        return {"message": "Course not found in the dashboard"}


@router.post("/Admin/add_unit")
def add_unit_to_course_endpoint(course_id: int, title: str, db: Session = Depends(get_db_session)):
    unit = add_unite_to_course(course_id, title, db)
    if unit:
        return {"message": "unit added successfully"}
    else:
        return {"message": "unit already exists in the dashboard"}

@router.get("/Student/get_units")
def get_unit_by_course_id_endpoint(course_id: int, db: Session = Depends(get_db_session)):
    units = get_unite_by_course_id(course_id, db)
    result = []
    for unit in units:
        result.append({
            "id": unit.id,
            "title": unit.title,
        })
    return result

# @app.delete("/unit/{unit_id}")
# def delete_unit_from_course_endpoint(unit_id: int, db: Session = Depends(get_db_session)):
#     result = delete_unit_from_course(unit_id, db)
#     return {"message": "Unit deleted from the course successfully"}

"""
ask ahamd how can delete unit from course : 
i cant delete unit directly because the unit is linked to the lessons 
"""


@router.post('/Admin/add_lesson')
def add_lesson_to_unit_endpoint( title :str , db:Session =Depends(get_db_session)):
    lesson =add_lesson_to_dashbord(title,db)
    if lesson:
        return {"message": "lesson added successfully"}
    else:
        return {"message": "lesson already exists in the dashboard"}


@router.get("/Student/get_lesson")
def get_lesson_endpoint(unit_id:int,db:Session=Depends(get_db_session)):
    lessons=get_lesson_by_unit_id(unit_id,db)
    lessons_by_unit=[]
    for lesson in lessons:
        lessons_by_unit.append({
            "id": lesson.id,
            "title": lesson.title,
        })
    return lessons_by_unit


@router.post("/Admin/lessons/{lesson_id}/upload-video")
def add_video_material_by_lesson_id(lesson_id: int,file: UploadFile = File(...),db: Session = Depends(get_db_session)):
    existing_video = db.query(Material).filter(Material.lesson_id == lesson_id,Material.type == "video").first()
    if existing_video:
        return {"message": "video already exists for this lesson"}
    file_data = file.file.read()

    new_material = Material(
        lesson_id=lesson_id,
        type="video",
        file_data=file_data,
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return {
        "message": "video uploaded successfully",
        "material_id": new_material.id
    }

@router.post("/Admin/lessons/{lesson_id}/upload-pdf")
def add_pdf_material_by_lesson_id(lesson_id: int,file: UploadFile = File(...),db: Session = Depends(get_db_session)):
    existing_video = db.query(Material).filter(Material.lesson_id == lesson_id,Material.type == "pdf").first()
    if existing_video:
        return {"message": "pdf already exists for this lesson"}
    file_data = file.file.read()

    new_material = Material(
        lesson_id=lesson_id,
        type="pdf",
        file_data=file_data,
    )
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return {
        "message": "pdf uploaded successfully",
        "material_id": new_material.id
    }

@router.get("/Student/get_video")
def get_video_by_lesson_id(lesson_id: int,db: Session = Depends(get_db_session)):
    video = db.query(Material).filter( Material.lesson_id == lesson_id,Material.type == "video").first()
    if not video:
        return {"error": "Video not found"}

    return Response(
        content=video.file_data,
        media_type="video/mp4"
    )
@router.get("/Student/pdf")
def get_pdf_by_lesson_id(lesson_id: int,db: Session = Depends(get_db_session)):
    pdf = db.query(Material).filter(Material.lesson_id == lesson_id,Material.type == "pdf").first()
    if not pdf:
        return {"error": "PDF not found"}

    return Response(
        content=pdf.file_data,
        media_type="video/mp4"
    )



