from fastapi import FastAPI
from .routers import posts, photos

app = FastAPI()

app.include_router(posts.router)
app.include_router(photos.router)
