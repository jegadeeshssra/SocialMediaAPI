from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import models
from .database.db import engine
from .routers import users , posts , auth , votes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

# Your API responds with headers like Access-Control-Allow-Origin:*,Access-Control-Allow-Methods:*,etc., 
# telling browsers "yes, this cross-origin request is OK."
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")   
async def latest_posts():
    return {
        "message":"SocialMediaAPI"
    }

