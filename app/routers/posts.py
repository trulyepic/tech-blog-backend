from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter(prefix="/posts", tags=["Posts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.PostOut)
def create(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)


@router.get("/", response_model=list[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)


@router.get("/{slug}", response_model=schemas.PostOut)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = crud.get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = crud.update_post(db, post_id, updated_post)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.delete_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": f"Post with ID {post_id} deleted."}