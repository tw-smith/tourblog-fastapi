from fastapi import APIRouter, Response
from app.db.db import select_post, select_all_posts, select_posts_by_tag, select_photos_by_post, select_photo_by_photo_id
from app.db.entities import Post as DBPost, Photo as DBPhoto
from .entities import IndexPost, Post, Photo
import json

router = APIRouter()


@router.get("/api/posts-index/all")
def get_all_posts():
    posts: list[IndexPost] = []
    for post in select_all_posts():
        posts.append(from_db_index_post(post))
    
    return posts

@router.get("/api/posts-index/{tag}")
def get_posts_by_tag(tag: str):
    posts: list[IndexPost] = []
    for post in select_posts_by_tag(tag):
        posts.append(from_db_index_post(post))
    return posts

@router.get("/api/posts/{slug}")
def get_post(slug: str, response: Response):
    post = select_post(slug)
    
    if post == None:
        return "Post not found"
    response.headers["Cache-Control"] = "max-age=604800"
    return [from_db_post(post)]


def from_db_index_post(db_post: DBPost) -> IndexPost:
    
    photo = select_photo_by_photo_id(db_post.cover_photo_id)
    
    if photo == None:
        coverPhotoURL = ""
    else:
        coverPhotoFormats = photo.formats.get("small")
        if coverPhotoFormats == None:
            coverPhotoURL = ""
        else:
            coverPhotoURL = coverPhotoFormats["url"]
       
    return IndexPost(
        id=db_post.id,
        title=db_post.title,
        tag=db_post.tag,
        slug=db_post.slug,
        publishedAt=db_post.published_at,
        displayDate=db_post.display_date,
        coverPhoto=coverPhotoURL
    )
  
def from_db_photo(db_photo: DBPhoto) -> Photo:
    return Photo(
        id=db_photo.id,
        caption=db_photo.caption,
        url=db_photo.url,
        formats=db_photo.formats
    )
    
    
    
def from_db_post(db_post: DBPost) -> Post:
    db_photos = select_photos_by_post(db_post.id)
    
    photos: list[Photo] = []
    for photo in db_photos:
        photos.append(from_db_photo(photo))
    
    return Post(
        id=db_post.id,
        title=db_post.title,
        subtitle=db_post.subtitle,
        tag=db_post.tag,
        slug=db_post.slug,
        content=db_post.content,
        publishedAt=db_post.published_at,
        displayDate=db_post.display_date,
        photos=photos        
    )
    