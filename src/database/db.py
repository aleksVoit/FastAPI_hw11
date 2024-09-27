import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..conf.config import settings

SQLALCHEMY_DB_URL = settings.sqlalchemy_db_url

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
