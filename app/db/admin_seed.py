from app.db.database import SessionLocal
from sqlalchemy import select

from app.core.Config import settings
from app.core.password_hasher import hash_password
from app.models.user import User

def create_admin()->None:
    with SessionLocal() as db:
        existing_user=db.query(User).filter(User.email==settings.admin_email).first()
        if existing_user:
            if existing_user.role =="admin":
                print("admin already exists")
                return
            raise RuntimeError(
                "The admin email already belongs to a student."
            )

        admin=User(
            name=settings.admin_name,
            email=settings.admin_email,
            password=hash_password(settings.admin_password),
            role="admin",

        )
        db.add(admin)
        db.commit()
        print("admin created successfully ")

if __name__ == "__main__":
    create_admin()
