from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email==email,User.is_deleted.is_(False)).first()

    def get_student_by_id(self, student_id: int) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.id == student_id,
                User.role == "student",
                User.is_deleted.is_(False),
            )
            .first()
        )

    def list_students(self) -> list[User]:
        return (self.db.query(User).filter(User.role == "student"
                                           ,User.is_deleted.is_(False)).all())

    def add(
        self,
        name: str,
        email: str,
        password: str,
        role: str,
    ) -> User:
        user = User(
            name=name,
            email=email,
            password=password,
            role=role,
        )
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)

    def soft_delete(self, user: User) -> None:
        user.is_deleted = True





__all__ = ["UserRepository"]
