from typing import Optional, List
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, schemas,utils, oauth2
from fastapi import FastAPI, Response,status, HTTPException, Depends, APIRouter
from sqlalchemy import func, or_

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/", response_model=List[schemas.PostResponse_alt])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
               limit: Optional[int] = 10, skip: Optional[int] = 0, q: Optional[str] = ''):
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.execute(
    #     'select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id  group by posts.id')
    # results = []
    # for post in posts:
    #     results.append(dict(post))
    # print(results)
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(q)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # created_post=connection.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published)).fetchone()
    # print(post.dict())
    # new_post=models.Post(title=post.title, content=post.content, published=post.published)

    new_post=models.Post(owner_id = current_user.id, **post.dict()) # the ** is to unpack the dictionary
    # print(new_post.__dict__)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #
    return new_post



@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Retrieve the post from the database
    # post = connection.execute("SELECT * FROM posts WHERE id = %s", (post_id,)).fetchone()
    post=db.query(models.Post).filter(models.Post.id==post_id).first()
    
    # Check if the post was found
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # deleted_post=connection.execute("DELETE FROM posts WHERE id= %s RETURNING *", (post_id,)).fetchone()
    # connection.commit()
    # print(deleted_post)

    post_query=db.query(models.Post).filter(models.Post.id==post_id)

    if post_query.first() is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    # updated_post = connection.execute("UPDATE posts SET title = %s, content = %s, id = %s WHERE id = %s RETURNING *", (post.title, post.content, post_id, post_id)).fetchone()
    # connection.commit()

    post_query=db.query(models.Post).filter(models.Post.id==post_id)
    if post_query.first() is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this post")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
   
    return post_query.first()
