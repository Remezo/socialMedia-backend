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
from app.oauth2 import create_access_token
import logging

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


@pytest.fixture(scope="function")
def test_user(client):
    user=schemas.UserCreate(email="test2@gmail.com",password="password123")
  
    response=client.post("/users/",json= user.dict())
    new_user=response.json()
    new_user['password']=user.password   
    print(new_user)
    assert response.status_code==201
    return new_user
    

@pytest.fixture(scope="function")
def token(test_user):
    access_token = create_access_token({"user_id": test_user['id']})
    return access_token

@pytest.fixture(scope="function")
def authorized_client(client, token):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture(scope="function")
def test_posts(session, test_user):

    posts=[{
        "title":"Post 1",
        "content":"Content 1",
        "owner_id":test_user['id']
    },{
        "title":"Post 2",
        "content":"Content 2",
        "owner_id":test_user['id']
    },
    {
        "title":"Post 3",
        "content":"Content 3",
        "owner_id":test_user['id']
    }]
    
    session.add_all([models.Post(**post) for post in posts])
    session.commit()
    posts=session.query(models.Post).all()
    return posts