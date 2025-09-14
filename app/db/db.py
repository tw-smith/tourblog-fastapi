from sqlmodel import Session, create_engine, select, col, asc
from .entities import Post, Photo
from sqlalchemy import text

engine = create_engine("postgresql://admin:admin@postgresdb:5432/tourblog-fastapi", echo=True)


def select_post(slug: str):
    with Session(engine) as session:
        statement = select(Post).where(col(Post.slug) == slug)
        results = session.exec(statement)
        return results.first()
    
def select_all_posts():
    with Session(engine) as session:
        statement = select(Post).order_by(asc(Post.display_date))
        results = session.exec(statement)
        return results.all()
    
def select_posts_by_tag(tag: str):
    with Session(engine) as session:
        statement = select(Post).order_by(asc(Post.display_date)).where(col(Post.tag) == tag)
        results = session.exec(statement)
        return results.all()
    
def select_photos_by_post(post_id: int):
    with Session(engine) as session:
        statement = f"SELECT photo_id FROM post_photos WHERE post_photos.post_id = {post_id}"
        post_photos = session.execute(text(statement)).scalars().all()
       # post_photos = session.exec(select(PostPhotos).where(col(PostPhotos.post_id) == post_id)).all() 
        
        photo_ids = [0] # Needed to do this to get round type hinting. Couldn't find a way to do list[int]
        for pp in post_photos:
            photo_ids.append(pp)
        photo_ids.remove(0)
        
        return session.exec(select(Photo).where(col(Photo.id).in_(photo_ids))).all()
    
def select_photo_by_photo_id(photo_id: int):
    with Session(engine) as session:
        statement = select(Photo).where(col(Photo.id) == photo_id)
        results = session.exec(statement)
        return results.first()
        