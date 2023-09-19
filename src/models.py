import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    name = Column(String(50), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(30), nullable=False)
    pronouns = Column(String(30), nullable=True)
    bio = Column(String(150), nullable=True)
    gender = Column(String(10), nullable=True)
    account_type = Column(String(30), nullable=True)

    def serialize(self):
        return {
            "username": self.username,
            "name": self.name,
            "pronouns": self.pronouns,
            "bio": self.bio,
            "gender": self.gender,
            "account_type": self.account_type
        }

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    used_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    def serialize(self):
        return {
            "user_id": self.user_id,
        }

class Following(Base):
    __tablename__ = 'following'
    id = Column(Integer, primary_key=True)
    used_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(User)

    def serialize(self):
        return {
            "user_id": self.user_id,
        }
    
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user = relationship(User)
    user_id = Column(Integer, ForeignKey("user.id"))
    image = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=False)
    location = Column(String(75), nullable=True)
    timestamp = Column(Integer, nullable=False)
    visibility = Column(Integer, nullable=False)

    def serialize(self):
        return {
            "image": self.image,
            "description": self.description,
            "location": self.location,
            "timestamp": self.timestamp,
            "visibility": self.visibility
        }
    
class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user = relationship(User)
    post_id = Column(Integer, ForeignKey("post.id"))
    
    def serialize(self):
        return {
        }

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user = relationship(User)
    containing_post = Column(Integer, ForeignKey("post.id"))
    containing_comment_id = Column(Integer, nullable=True)
    timestamp = Column(Integer, nullable=False)
    visibility = Column(Integer, nullable=False)
    comment_content = Column(String(1000), nullable=False)

    def serialize(self):
        return {
            "containing_comment_id": self.containing_comment_id,
            "timestamp": self.timestamp,
            "visibility": self.visibility,
            "comment_content": self.comment_content
        }

class Share(Base):
    __tablename__ = 'share'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))
    share_via = Column(String(50), nullable=False)
    share_content = Column(String(1000), nullable=True)

    def serialize(self):
        return {
            "share_via": self.share_via,
            "share_content": self.share_content
        }


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e