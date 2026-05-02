from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from Config import settings

engine = create_engine(settings.database_url)

session_factory = sessionmaker(bind=engine,autocommit=False)
SessionLocal = session_factory

def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        #===================================================
        session.commit()
    finally:
        session.close()

__all__=["get_db_session"]




