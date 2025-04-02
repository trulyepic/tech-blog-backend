from fastapi import FastAPI
from .routers import posts, users
from .database import Base, engine
from .models import Post  # Make sure this line exists to register the model
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tech Tutorials + Toolkits Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to Tech Tutorials + Toolkits Hub!"}
