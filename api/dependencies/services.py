from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db_session
from repositories.course_repository import CourseRepository
from repositories.material_repository import MaterialRepository
from repositories.user_courses_repository import UserCourseRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService
from services.course_service import CourseService
from services.deletion_policies import SoftDeleteStudentDeletionPolicy
from services.enrollment_service import EnrollmentService
from services.material_service import MaterialService
from services.student_admin_services import StudentAdminService
from services.token_service import TokenService


def get_material_service(
    db: Session = Depends(get_db_session),
) -> MaterialService:
    return MaterialService(MaterialRepository(db))


def get_auth_service(
    db: Session = Depends(get_db_session),
) -> AuthService:
    return AuthService(UserRepository(db))


def get_token_service() -> TokenService:
    return TokenService.from_settings()


def get_student_admin_service(
    db: Session = Depends(get_db_session),
) -> StudentAdminService:
    users = UserRepository(db)
    return StudentAdminService(
        users=users,
        deletion_policy=SoftDeleteStudentDeletionPolicy(users),
    )


def get_course_service(
    db: Session = Depends(get_db_session),
) -> CourseService:
    return CourseService(CourseRepository(db))


def get_enrollment_service(
    db: Session = Depends(get_db_session),
) -> EnrollmentService:
    return EnrollmentService(
        courses=CourseRepository(db),
        enrollments=UserCourseRepository(db),
    )
