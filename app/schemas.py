#title str and content str, category are required fields
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    timestamp: datetime
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    # rating: Optional[int] = None    

class PostCreate(PostBase):
   pass

class PostResponse(PostBase):
    id: int
    owner_id: int
    owner: UserResponse
    class Config:
        from_attributes = True

class PostResponse_alt(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        from_attributes = True

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    timestamp: datetime
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
    class Config:
        from_attributes = True