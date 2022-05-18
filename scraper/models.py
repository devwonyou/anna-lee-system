from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

class PKModel(SQLModel):
  """Base model class that adds a 'primary key' column named ``id``."""
  id: Optional[int] = Field(default=None, primary_key=True)


class CreatorLinkBase(SQLModel):
  followed_id: Optional[int] = Field(foreign_key='creator.id', default=None, primary_key=True)
  follower_id: Optional[int] = Field(foreign_key='creator.id', default=None, primary_key=True)

class CreatorLinkCreate(CreatorLinkBase):
  followed_id: int
  follower_id: int

class CreatorLinkUpdate(CreatorLinkBase):
  pass

class CreatorLinkInDBBase(CreatorLinkBase):
  pass

class CreatorLink(CreatorLinkInDBBase, table=True):
  pass


class CreatorBase(SQLModel):
  username: Optional[str] = Field(
    max_length=30,
    sa_column=Column(String, unique=True)
  )
  is_manually_added: Optional[bool] = False

class CreatorCreate(CreatorBase):
  username: str

class CreatorUpdate(CreatorBase):
  pass

class CreatorInDBBase(CreatorBase, PKModel):
  pass

class Creator(CreatorInDBBase, table=True):
  following_list: List["Creator"] = Relationship(
    back_populates="follower_list",
    link_model=CreatorLink,
    sa_relationship_kwargs=dict(
      primaryjoin="creator.id==creatorlink.follower_id",
      secondaryjoin="creator.id==creatorlink.followed_id",
    ),
  )
  follower_list: List["Creator"] = Relationship(
    back_populates="following_list",
    link_model=CreatorLink,
    sa_relationship_kwargs=dict(
      primaryjoin="creator.id==creatorlink.followed_id",
      secondaryjoin="creator.id==creatorlink.follower_id",
    ),
  )

CreatorLink.update_forward_refs()
Creator.update_forward_refs()