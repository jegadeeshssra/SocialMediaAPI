from fastapi import FastAPI , Response , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session

from ..models import models

from .. import schemas
from ..database.db import engine , get_db
from ..utils import hashing

router = APIRouter(
    prefix="/users",
    tags=['Users']
) 

# As the prefix is /users, the path will be /users/ , so when the request is sent to /users it will respond with 307 Temporary Redirect and then goes to the path /users/
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.CreateUserResponse)
async def create_users(payload: schemas.CreateUser, db: Session = Depends(get_db)):
    user_check_query = db.query(models.User).filter(models.User.email == payload.email)
    user_data  = user_check_query.first()
    if user_data != None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"This email id - {payload.email} already exists"
        )
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
