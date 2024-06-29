
from typing import Optional, List
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas,utils, oauth2
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=404, detail="Post not found")

    vote_query=db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)



    if (vote.dir ==1):
        if vote_query.first():
            raise HTTPException(status_code=409, detail= f"You- {current_user.id} have already upvoted this post")
        new_vote=models.Vote(user_id = current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Upvoted successfully"}

    else:
        if vote_query.first() is None:
            raise HTTPException(status_code=409, detail= f"You- {current_user.id} have already downvoted this post")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Downvoted successfully"}
   


