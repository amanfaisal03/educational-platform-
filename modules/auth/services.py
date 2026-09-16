from fastapi import Depends
from sqlalchemy.orm import Session

from modules.database import get_db_session
from modules.courses.course.course_repository import CourseRepository
from modules.courses.material.material_repository import MaterialRepository
from modules.users.user_course.user_courses_repository import UserCourseRepository
from modules.users.repository import UserRepository
from modules.auth.Services import AuthService
from modules.courses.course.service import CourseService
from modules.deletion_policies import SoftDeleteStudentDeletionPolicy
from modules.users.user_course.enrollment_service import EnrollmentService
from modules.courses.material.material_service import MaterialService
from modules.users.admin.student_admin_services import StudentAdminService
from modules.auth.token_service import TokenService


def get_material_service(
    db: Session = Depends(get_db_session),
):
    return MaterialService(
        repository=MaterialRepository(db),
        enrollments=UserCourseRepository(db),
    )


def get_auth_service(
    db: Session = Depends(get_db_session)) :
    return AuthService(UserRepository(db))


def get_token_service() :
    return TokenService.from_settings()


def get_student_admin_service(
    db: Session = Depends(get_db_session),
) :
    users = UserRepository(db)
    return StudentAdminService(
        users=users,
        deletion_policy=SoftDeleteStudentDeletionPolicy(users),
    )


def get_course_service(
    db: Session = Depends(get_db_session),
):
    return CourseService(CourseRepository(db))


def get_enrollment_service(
    db: Session = Depends(get_db_session),
):
    return EnrollmentService(
        courses=CourseRepository(db),
        enrollments=UserCourseRepository(db),
    )
