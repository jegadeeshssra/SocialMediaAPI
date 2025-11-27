from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session

# jwt   
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from ..models import models

from ..database.db import get_db
from .. import schemas
from ..config.config import settings

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Creates a FastAPI security utility that automatically extracts a Bearer token from the 
# Authorization header and makes it available via Depends(oauth2_scheme), while powering the login form in /docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# tokenUrl="login" is only for the Swagger UI login form – it tells the docs: "send username/password to /token to get a token".
# The actual token extraction works on EVERY protected endpoint (like /users/me, /posts, etc.) because FastAPI automatically runs oauth2_scheme whenever you use Depends(oauth2_scheme) in a route — completely independent of the path.

def create_access_token(data: dict):
    access_token_expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()     # so that data dict is replicated in memory for modification.
    if access_token_expires_delta:
        expire = datetime.now(timezone.utc) + access_token_expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # returns a str - header.payload.signature
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# token: str = Depends(oauth2_scheme)
# extracts the token from HTTP headers
# "Authorization" : "Bearer <TOKEN>"

def verify_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        # This is an official HTTP standard header (RFC 7235) used only in 4xx/5xx responses to indicate what authentication method the server expects.
        # In OAuth2/JWT, "Bearer" is the standard — it tells clients: "Send a token in the header, not a username/password."
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Verifies the JWT’s signature and expiration using the secret key, then returns the decoded payload as a dictionary — or raises an error if anything is invalid.
        # payload = {'sub': 'j@gmail.com', 'exp': 1763980168}
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # dict
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return email

def get_user_with_email(email: str, db: Session):
    user_query = db.query(models.User).filter(models.User.email == email)
    user = user_query.first() # <class 'src.models.User'>
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with EMAIL ID -  {email} not found"
        )
    return user

# FastAPI's dependency injection only resolves Depends() at runtime when the function is called as part of an endpoint or chained dependency — not when called directly like a regular Python function.
def get_current_user(email: str = Depends(verify_user), db: Session = Depends(get_db)):
    current_user = get_user_with_email(email,db)
    return current_user