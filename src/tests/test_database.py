from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient

from ..config.config import settings
from ..main import app 
from ..database.db import get_db
from ..models import models

print("DB URL:", settings.USER_NAME, settings.PASSWORD, settings.DB)
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<db_name>"
SQLALCHEMY_DATABASE_URL = f"{settings.DB}://{settings.USER_NAME}:{settings.PASSWORD}@{settings.HOST}/{settings.DB_NAME}_TEST"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Default scope of this fixture is destroyed at the end of each test
@pytest.fixture(scope="session")
def client():
    # Get the Base from models.py instead of db.py for creating the tables
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    def get_test_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    # overides the get_db function with get_test_db function for directing the api to use the test database
    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app) # - This TestClient will simulate the requests to the API.






