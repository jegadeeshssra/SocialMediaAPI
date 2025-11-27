from fastapi import Response , status , HTTPException , Depends , APIRouter
from typing import List
from sqlalchemy.orm import Session

from ..models import models

from .. import schemas
from ..database.db import get_db
from ..utils import oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

# current_user : bool = Depends(oauth2.get_current_user)
# - This would verify the auth jwt token wihtin request's "Authorization" header

@router.post("/")
async def get_posts(payload: schemas.Vote ,db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_chk_query = db.query(models.Post).filter(models.Post.id == payload.post_id)
    post = post_chk_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"posts with id - {payload.post_id} is not found"
        )
    vote_chk_query = db.query(models.Votes).filter(models.Votes.post_id == payload.post_id and models.Votes.user_id == current_user.id)
    vote_chk = vote_chk_query.first()
    if payload.vote_direction == 1:
        if vote_chk:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"This post id - {payload.post_id} is already been liked by the user id - {current_user.id}"
            )
        new_vote = models.Votes(post_id=payload.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        if new_vote == None:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                details="Unable to like the post"
                )
        return {"message": "successfully added vote"}
    else:
        if not vote_chk:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Vote does not exist"
                )
        vote_chk_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}



