from fastapi import FastAPI

from .models import models
from .database.db import engine
from .routers import users , posts , auth , votes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(votes.router)



