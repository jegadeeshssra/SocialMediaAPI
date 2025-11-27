from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config.config import settings

DB = settings.DB
DB_NAME = settings.DB_NAME
USERNAME = settings.USER_NAME
PASSWORD = settings.PASSWORD
HOST = settings.HOST

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<db_name>"
SQLALCHEMY_DATABASE_URL = f"{DB}://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

