from sqlalchemy.orm import Session
from app.models import Course, Unit, Lesson

def add_course_to_dashbord(name: str, db: Session):
    existing_course = db.query(Course).filter_by(name=name).first()
    if existing_course:
        return {"message": "Course already exists in the dashboard"}

    new_course = Course(name=name)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"message": "Course added to the dashboard successfully"}


def delete_course_from_dashboard(course_id: int, db: Session):
    course = db.query(Course).filter_by(id=course_id).first()
    if course:
        db.delete(course)
        db.commit()
        return {"message": "Course deleted from the dashboard successfully"}
    return {"message": "Course not found in the dashboard"}


def add_unite_to_course(course_id: int, title: str, db: Session):
    course = db.query(Course).filter_by(id=course_id).first()
    if not course:
        return {"message": "Course not found in the dashboard"}

    new_unit = Unit(title=title, course_id=course_id)
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return {"message": "Unit added to the course successfully"}

def add_lesson_by_unite(unite_id: int, title: str, db: Session):
    existing_lesson =db.query(Lesson).filter_by(title=title).first()
    if existing_lesson:
        return {"message": "lesson already exists in the dashboard"}

    new_lesson = Lesson(title=title,unite_id=unite_id)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return {"message": "lesson added to the dashboard successfully"}
