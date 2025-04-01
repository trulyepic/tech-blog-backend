from sqlalchemy.orm import Session
from app import models, schemas


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_post_by_slug(db: Session, slug: str):
    return db.query(models.Post).filter(models.Post.slug == slug).first()

def update_post(db: Session, post_id: int, post_data: schemas.PostCreate):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return None
    for key, value in post_data.model_dump().items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return None
    db.delete(post)
    db.commit()
    return post