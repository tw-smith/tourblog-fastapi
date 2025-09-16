from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import posts, photos

app = FastAPI()

origins = [
    "https://www.cycling-south.com",
    "https://cycling-south.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts.router)
app.include_router(photos.router)
