from fastapi import Response , status , HTTPException , Depends , APIRouter
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import models

from .. import schemas
from ..database.db import get_db
from ..utils import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# current_user : bool = Depends(oauth2.get_current_user)
# - This would verify the auth jwt token wihtin request's "Authorization" header

@router.get("/",response_model= List[schemas.ResponsePost])
async def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: str = ""):
    all_posts = db.query(
        models.Post,func.count(models.Votes.post_id).label("votes")
        ).join(
            models.Votes,models.Votes.post_id == models.Post.id, isouter= True
            ).group_by(
                models.Post.id
                ).filter(
                    models.Post.content.contains(search)
                    ).limit(limit).offset(skip).all()
    print(type(all_posts)) # query object
    print(str(all_posts)) # SQL statement
    if all_posts == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are zero posts"
        )   
    return all_posts

# Order of the api endpoint definition matters - /posts/{id} should not be before /posts/latest bcuz the /latest will be taken as id path parameter
# @router.post("/")
# async def latest_posts():
#     return {
#         "message":"SocialMediaAPI"
#     }

@router.get("/{id}", response_model = schemas.ResponsePost)
async def get_posts_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id - {id} not found"
        )
    if current_user.id != post.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to access this post"
        )
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ResponsePost)
#async def create_posts(payload : dict = Body(...)):
async def create_posts(payload: schemas.PostBase, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    print(type(current_user)) # <class 'src.models.User'>
    new_post = models.Post(**payload.model_dump(),user_id = current_user.id) # ** - unpacks the dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # this return the created post with automtic values of id and created_at
    if new_post == None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Unable to create the post"
        )
    return new_post


@router.put("/{id}", response_model= schemas.ResponsePost)
async def update_posts(id: int, payload: schemas.PostBase, db: Session = Depends(get_db), current_user :  models.User = Depends(oauth2.get_current_user)):
    new_post_dict = payload.model_dump()
    post_query = db.query(models.Post).filter(models.Post.id == id) # only builds the query(query object(lazy SQL builder))
    post = post_query.first()    # actually hits the database NOW
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id - {id} not found. Updation is INVALID"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to update this post"
        )
    new_post_dict["user_id"] = current_user.id
    post_query.update(new_post_dict, synchronize_session = False) # sych... - it does not update the session's identity map and executes directly to the DB
    db.commit()
    db.refresh(post)
    return post     # Its an Post Model OBJECT


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db : Session = Depends(get_db), current_user :  models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id - {id} not found."
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to delete this post"
        )
    post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)

