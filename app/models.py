from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column

import datetime


class Base(DeclarativeBase):
    pass

class Post(Base):

    __tablename__ = "posts"
    id = mapped_column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    owner_id = mapped_column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable=False)
    title = mapped_column(String, nullable=False)
    content = mapped_column(String, nullable=False)
    published = mapped_column(Boolean,server_default='true', nullable=False)
    timestamp = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner=relationship("User")  

class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    email = mapped_column(String, nullable=False, unique=True)
    password = mapped_column(String, nullable=False)
    timestamp = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class Vote(Base):
    __tablename__ = "votes"
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key=True)
    post_id = mapped_column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key=True)
    
    timestamp = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user=relationship("User")
    post=relationship("Post")