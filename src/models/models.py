from sqlalchemy import Column, Integer, Boolean, String , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null , text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..database.db import Base
from ..config.config import settings

# Just Initial Creation and NO column modification
class Post(Base):
    __tablename__ = f"{settings.POSTS_TABLE_NAME}"
    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String , nullable= False)
    content = Column(String , nullable= False)
    published = Column(Boolean , server_default= "True", nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    # CASCADE - when an user is deleted , posts associated with that user id is also deleted.
    user_id = Column(Integer, ForeignKey(f"{settings.USERS_TABLE_NAME}.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = f"{settings.USERS_TABLE_NAME}"
    id = Column(Integer, primary_key=True, nullable= False)
    email = Column(String, nullable= False)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), server_default=text('now()'), nullable= False)
    

class Votes(Base):
    __tablename__ = f"{settings.VOTES_TABLE_NAME}"
    post_id = Column(Integer, ForeignKey(
        f"{settings.POSTS_TABLE_NAME}.id",
        ondelete="CASCADE"
        ), primary_key=True
    )
    user_id = Column(Integer, ForeignKey(
        f"{settings.USERS_TABLE_NAME}.id",
        ondelete="CASCADE"
        ), primary_key=True
    )

# making 2 columns as primary keyas will make them composite keys(each can have duplicates separately but should be unique when combined)