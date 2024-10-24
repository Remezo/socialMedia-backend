from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database import engine
from app.models import Base
from app.models import User
from app import schemas
from app.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import psycopg
from psycopg.rows import dict_row
from app.database import get_db
from app import models

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Depine123@localhost/fastapi"
SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL) #this is what responsible to connect to a database.
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# this is to talk to a session to the database.

models.Base.metadata.create_all(bind=engine) #this is to create the tables in the database.



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
    