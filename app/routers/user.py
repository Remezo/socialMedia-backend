
from typing import Optional, List
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas,utils, oauth2
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #hash the password
    hashed_password = utils.hash_password(user.password)
    user.password=hashed_password

    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_email(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id :{id} found")
    return user

