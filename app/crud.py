from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.utils.auth import hash_password, verify_password


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.model_dump(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Post)
        .options(joinedload(models.Post.user))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_post_by_slug(db: Session, slug: str):
    return (
        db.query(models.Post)
        .options(joinedload(models.Post.user))
        .filter(models.Post.slug == slug)
        .first()
    )


def get_posts_by_user(db: Session, user_id: int):
    return (
        db.query(models.Post)
        .options(joinedload(models.Post.user))
        .filter(models.Post.user_id == user_id)
        .all()
    )


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


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
