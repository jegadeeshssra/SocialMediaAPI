from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..config.config import settings
print("DB URL:", settings.USER_NAME, settings.PASSWORD, settings.DB)
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<db_name>"
SQLALCHEMY_DATABASE_URL = f"{settings.DB}://{settings.USER_NAME}:{settings.PASSWORD}@{settings.HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

