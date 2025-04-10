# routes/sitemap.py
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models import Post

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/sitemap.xml", response_class=Response)
async def sitemap_xml(db: Session = Depends(get_db)):
    base_url = "https://codesprig.com"
    posts = db.query(Post).all()

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f"<url><loc>{base_url}/</loc><priority>1.0</priority></url>"]

    # Homepage

    # Static pages
    static_paths = ["/privacy-policy", "/terms", "/contact"]
    for path in static_paths:
        xml.append(f"<url><loc>{base_url}{path}</loc><priority>0.5</priority></url>")

    # Blog posts
    for post in posts:
        url = f"{base_url}/posts/{post.slug}"
        lastmod = (post.updated_at or post.created_at or datetime.utcnow()).date()
        xml.append(
            f"<url><loc>{url}</loc><lastmod>{lastmod}</lastmod><priority>0.8</priority></url>"
        )

    xml.append("</urlset>")
    return Response(content="\n".join(xml), media_type="application/xml")


@router.get("/robots.txt", response_class=Response)
async def robots_txt():
    return Response(
        content="User-agent: *\nAllow: /\nSitemap: https://codesprig.com/sitemap.xml",
        media_type="text/plain"
    )
