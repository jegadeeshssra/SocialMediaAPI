from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session

from .. import models , schemas
from ..db import engine , get_db
from ..utils import hashing

router = APIRouter(
    prefix="/users",
    tags=['Users']
) 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.CreateUserResponse)
async def create_users(payload: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_pwd = hashing.hash_password(payload.password)
    payload.password = hashed_pwd
    new_user = models.User(**payload.model_dump()) # unpack the dict
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # this return the created post with automtic values of id and created_at
    if new_user == None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Unable to create the user"
        )
    return new_user
