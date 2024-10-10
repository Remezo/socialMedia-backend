from typing import Optional, List
from fastapi import FastAPI, Response,status, HTTPException, Depends
from fastapi import Body

from random import randrange
import psycopg
from psycopg.rows import dict_row
from .database import engine, get_db
from . import models, schemas,utils, config
from sqlalchemy.orm import Session
from .routers import post, user,auth, vote
import logging
from fastapi.middleware.cors import CORSMiddleware


# Set the logging level for 'passlib' to ERROR
logging.getLogger('passlib').setLevel(logging.ERROR)




models.Base.metadata.create_all(bind=engine) #this is to create the tables in the database.

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


app.get("/")(lambda: {"Hello": "production ubuntu -tem"})
