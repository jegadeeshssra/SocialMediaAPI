from sqlalchemy import Column, Integer, Boolean, String , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null , text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .db import Base

USERS_TABLE_NAME = 'users'
POSTS_TABLE_NAME = "postsByORM"

# Just Initial Creation and NO column modification
class Post(Base):
    __tablename__ = f"{POSTS_TABLE_NAME}"
    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String , nullable= False)
    content = Column(String , nullable= False)
    published = Column(Boolean , server_default= "True", nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    # CASCADE - when an user is deleted , posts associated with that user id is also deleted.
    user_id = Column(Integer, ForeignKey(f"{USERS_TABLE_NAME}.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")

class User(Base):
    __tablename__ = f"{USERS_TABLE_NAME}"
    id = Column(Integer, primary_key=True, nullable= False)
    email = Column(String, nullable= False)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone= True), server_default=text('now()'), nullable= False)
    

