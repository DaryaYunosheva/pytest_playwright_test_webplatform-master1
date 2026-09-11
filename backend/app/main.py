from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import auth, users, news, comments
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5137",
        "http://localhost:3000",
        "http://127.0.0.1:5137",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(news.router)
app.include_router(comments.router)

@app.get("/")
def root():
    return {"message": "News Platform API"}
