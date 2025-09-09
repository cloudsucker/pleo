import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse

from app.models import Post

logger = logging.getLogger(__name__)
router = APIRouter()


posts = []


@router.get("/")
async def get_post_page():
    return HTMLResponse(
        open("app/static/pages/post.html", "r", encoding="utf-8").read(),
        200,
        {"Content-Type": "text/html"},
        media_type="text/html",
    )


@router.post("/")
async def add_post(content: Post):
    posts.append(content.text)
    return JSONResponse(
        {"message": "Post added successfully"},
        200,
        {"Content-Type": "application/json"},
        media_type="application/json",
    )
