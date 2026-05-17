from unicodedata import name
from fastapi import FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from fastapi import Depends
from models.database import get_db_session
from models.schema import Course, Unit, Lesson, Material
from fastapi.responses import HTMLResponse, RedirectResponse

def add_course_to_dashbord(name: str, db: Session = Depends(get_db_session)):
    existing_course = db.query(Course).filter_by(name=name).first()
    if existing_course:
        return {"message": "Course already exists in the dashboard"}

    new_course = Course(name=name)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"message": "Course added to the dashboard successfully"}


def delete_course_from_dashboard(course_id: int, db: Session = Depends(get_db_session)):
    course = db.query(Course).filter_by(id=course_id).first()
    if course:
        db.delete(course)
        db.commit()
        return {"message": "Course deleted from the dashboard successfully"}
    return {"message": "Course not found in the dashboard"}


def add_unite_to_course(course_id: int, title: str, db: Session = Depends(get_db_session)):
    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        return {"message": "Course not found in the dashboard"}

    new_unit = Unit(title=title, course_id=course_id)
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return {"message": "Unit added to the course successfully"}

# def delete_unit_from_course(unit_id: int, db: Session = Depends(get_db_session)):
#     unit = db.query(Unit).filter_by(id=unit_id).first()
#     if unit:
#         db.delete(unit)
#         db.commit()
#         return {"message": "Unit deleted from the course successfully"}
#     return {"message": "Unit not found in the course"}

def add_lesson_by_unite(unite_id:int,title:str, db: Session = Depends(get_db_session)):
    existing_lesson =db.query(Lesson).filter_by(title=title).first()
    if existing_lesson:
        return {"message": "lesson already exists in the dashboard"}

    new_lesson = Lesson(title=title,unite_id=unite_id)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return {"message": "lesson added to the dashboard successfully"}



def upload_material(lesson_id: int, file: UploadFile, Mtype: str, db: Session):
    existing = db.query(Material).filter(Material.lesson_id == lesson_id,Material.type == Mtype).first()

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    unit_id = lesson.unite_id

    if existing:
        return RedirectResponse(
            url=f"/admin/units/{unit_id}/lessons",
            status_code=303
        )

    material = Material(
        lesson_id=lesson_id,
        type=Mtype,
        file_data=file.file.read()
    )

    db.add(material)
    db.commit()

    return RedirectResponse(
        url=f"/admin/units/{unit_id}/lessons",
        status_code=303
    )
