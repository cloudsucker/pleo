import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse

from schemas import PostData

from db import SessionLocal
from models import Post

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_post_page():
    return HTMLResponse(
        open("app/static/pages/post.html", "r", encoding="utf-8").read(),
        200,
        {"Content-Type": "text/html"},
        media_type="text/html",
    )


@router.post("/")
async def add_post(post_data: PostData):

    db = SessionLocal()

    try:
        post = Post(author_id=post_data.author_id, content=post_data.text)
        db.add(post)
        db.commit()
        db.refresh(post)

        return JSONResponse(
            {
                "post_id": post.id,
                "message": "Post added successfully",
                "status": 200,
            },
            media_type="application/json",
        )

    finally:
        db.close()
