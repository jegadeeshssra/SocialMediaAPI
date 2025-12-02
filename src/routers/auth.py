from fastapi import status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from ..models import models

from .. import schemas
from ..database.db import get_db
from ..utils import hashing , oauth2

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
) 

# Creates a FastAPI security utility that automatically extracts a Bearer token from the 
# Authorization header and makes it available via Depends(oauth2_scheme), while powering the login form in /docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# tokenUrl="token" is only for the Swagger UI login form – it tells the docs: "send username/password to /token to get a token".
# The actual token extraction works on EVERY protected endpoint (like /users/me, /posts, etc.) because FastAPI automatically runs oauth2_schemewhenever you use Depends(oauth2_scheme) in a route — completely independent of the path.

# --- payload: OAuth2PasswordRequestForm = Depends() ---
# OAuth2PasswordRequestForm = type hint (tells FastAPI "expect an object of this class").
# For Depends() (no argument), it defaults to creating an instance of the type (OAuth2PasswordRequestForm).
# Only parses USERNAME and PASSWORD

@router.post("/login", response_model = schemas.UserLoginResponse)
async def create_users(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Retrieve the User's data with received email
    user_data = db.query(models.User).filter(models.User.email == payload.username).first()
    if user_data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user not found."
        )
    # Verify the hash
    if hashing.verify_password(payload.password,user_data.password) == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # create a JWT Token for this user
    jwt_access_token = oauth2.create_access_token({
        "sub" : user_data.email
    })
    return {
        "access_token" : jwt_access_token,
        "token_type" : "bearer",
        "id" : user_data.id,
        "email" : user_data.email,
        "created_at" : user_data.created_at
    }