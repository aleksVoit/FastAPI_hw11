import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import dotenv

env = dotenv.load_dotenv()

user = os.getenv("PG_USER")
pswd = os.getenv("PG_PASS")
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
db = os.getenv("PG_DB")

SQLALCHEMY_DB_URL = f'postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{db}'

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
