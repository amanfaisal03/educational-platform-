from sqlalchemy.orm import Session

from app.models import Course, UserCourse


class UserCourseRepository:
    """Persistence operations for student-course enrollment records."""

    def __init__(self, db: Session):
        self.db = db

    def get_enrollment(
        self,
        user_id: int,
        course_id: int,
    ) -> UserCourse | None:
        return (
            self.db.query(UserCourse)
            .filter(
                UserCourse.user_id == user_id,
                UserCourse.course_id == course_id,
            )
            .first()
        )

    def add(self, user_id: int, course_id: int) -> UserCourse:
        enrollment = UserCourse(user_id=user_id, course_id=course_id)
        self.db.add(enrollment)
        self.db.flush()
        self.db.refresh(enrollment)
        return enrollment

    def list_courses_for_student(self, user_id: int) -> list[Course]:
        return (
            self.db.query(Course)
            .join(UserCourse, Course.id == UserCourse.course_id)
            .filter(UserCourse.user_id == user_id)
            .all()
        )

    def delete_for_student(self, student_id: int) -> None:
        (
            self.db.query(UserCourse)
            .filter(UserCourse.user_id == student_id)
            .delete(synchronize_session=False)
        )


__all__ = ["UserCourseRepository"]
