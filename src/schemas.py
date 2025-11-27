from pydantic import BaseModel , EmailStr , ConfigDict
from typing import Literal
from datetime import datetime

# Register User
class CreateUser(BaseModel):
    email: EmailStr
    password: str

class CreateUserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)



# User Details
class UserOut(BaseModel):
    id : int
    email: str
    created_at: datetime



# User Login
class UserLogin(BaseModel):
    email : str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLoginResponse(BaseModel):
    id : int
    email: str
    created_at: datetime
    access_token: str
    token_type: str

    model_config = ConfigDict(
        from_attributes= True
    )


# Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None    
    model_config = ConfigDict(extra="forbid")

class Post(PostBase):
    user_id : int   

class ResponsePost(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    # class Config:           # OLD WAY
    #     orm_mode = True     # Pydantic model understands the ORM models to deserialize it into json
    # model_config = {                       # NEW WAY 
    #     "from_attributes" : True           # Pydantic model understands the ORM models to deserialize it into json
    # }
    owner: UserOut
    model_config = ConfigDict(from_attributes=True)

class Vote(BaseModel):
    post_id: int
    vote_direction: Literal[0, 1]