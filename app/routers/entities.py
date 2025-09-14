from __future__ import annotations
import datetime
from typing import Dict, Any
    
class IndexPost:
    id: int
    title: str
    tag: str
    slug: str
    publishedAt: datetime.datetime
    displayDate: datetime.datetime
    coverPhoto: str
    
    def __init__(
        self, 
        id: int, 
        title: str, 
        tag: str, 
        slug: str, 
        publishedAt: datetime.datetime, 
        displayDate: datetime.datetime,
        coverPhoto: str
    ):
        self.id = id
        self.title = title
        self.tag = tag
        self.slug = slug
        self.publishedAt = publishedAt
        self.displayDate = displayDate
        self.coverPhoto = coverPhoto
    
    
class Post:
    id: int
    title: str
    subtitle: str
    tag: str
    slug: str
    content: str
    publishedAt: datetime.datetime
    displayDate: datetime.datetime
    photos: list[Photo]
    
    def __init__(
    self, 
    id: int, 
    title: str, 
    subtitle: str, 
    tag: str, 
    slug: str, 
    content: str, 
    publishedAt: datetime.datetime, 
    displayDate: datetime.datetime,
    photos: list[Photo]
    ):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.tag = tag
        self.slug = slug
        self.content = content
        self.publishedAt = publishedAt
        self.displayDate = displayDate
        self.photos = photos
    
class Photo:
    id: int
    caption: str
    url: str
    formats: Dict[Any, Any]
    
    def __init__(
        self,
        id: int,
        caption: str,
        url: str,
        formats: Dict[Any, Any]      
    ):
        self.id = id
        self.caption = caption
        self.url = url
        self.formats = formats
    
class PhotoFormats:
    small: str
    large: str
    xlarge: str
    
    def __init__(
        self,
        small: str,
        large: str,
        xlarge: str
    ):
        self.small = small
        self.large = large
        self.xlarge = xlarge