from fastapi import FastAPI
from app.routers import posts, users, sitemap
from app.database import Base, engine
from app.models import Post  # Make sure this line exists to register the model
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tech Tutorials + Toolkits Hub")

origins = [
    "http://localhost:5173",          # Vite dev server
    "https://www.codesprig.com",      # Your production frontend
    "https://codesprig.com",          # Non-www version, just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(sitemap.router)
@app.get("/")
def root():
    return {"message": "Welcome to Tech Tutorials + Toolkits Hub!"}
