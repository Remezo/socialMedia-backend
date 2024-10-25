from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
from alembic import command

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Depine123@localhost/fastapi"
SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL) #this is what responsible to connect to a database.
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# this is to talk to a session to the database.



# Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db]=override_get_db


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()





# client=TestClient(app)

@pytest.fixture(scope="function")
def client(session):
    # models.Base.metadata.drop_all(bind=engine)
    # models.Base.metadata.create_all(bind=engine) #this is to create the tables in the database.

    def override_get_db():
        db = session
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)
    