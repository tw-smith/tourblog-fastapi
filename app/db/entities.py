from sqlmodel import SQLModel, Field
import datetime
#from sqlalchemy import JSON, Column
from sqlalchemy.dialects.postgresql import JSONB
#from typing import Dict


class Post(SQLModel, table=True):
    __tablename__: str = "posts" # type: ignore
    id: int = Field(default=None, primary_key=True)
    title: str
    subtitle: str
    tag: str
    slug: str
    content: str
    published_at: datetime.datetime
    display_date: datetime.datetime
    cover_photo_id: int


class Photo(SQLModel, table=True):
    __tablename__: str = "photos" # type: ignore
    id: int = Field(default=None, primary_key=True)
    name: str
    caption: str
    width: int
    height: int
    #formats: dict[Any, Any]
    #formats: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    formats: dict = Field(sa_type=JSONB, nullable=False)
    url: str
    
class PostPhotos(SQLModel, table=True):
    __tablename__: str = "post_photos" # type: ignore
    post_id: int = Field(primary_key=True)
    photo_id: int