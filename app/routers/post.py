import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

from schemas import PostData

from db import get_db, Session
from models import User, Post
from static import get_posts_html_page
from routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_post_page(user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=401)
    html_content = get_posts_html_page()
    return HTMLResponse(html_content)


@router.post("/")
async def add_post(
    post_data: PostData,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=401)

    post = Post(author_id=user.id, text=post_data.text)
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
