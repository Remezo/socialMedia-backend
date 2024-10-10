from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import psycopg
from psycopg.rows import dict_row
from .config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Depine123@localhost/fastapi"
SQLALCHEMY_DATABASE_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL) #this is what responsible to connect to a database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# this is to talk to a session to the database.

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     connection = psycopg.connect( host="localhost",
#                                           dbname="fastapi",
#                                           user="postgres",
#                                           password="Depine123",
#                                           row_factory=dict_row
#                                           )
#     print("Connection established")
# except (Exception, psycopg.Error) as error:
#         print("Error while connecting to PostgreSQL", error)
