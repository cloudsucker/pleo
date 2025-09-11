import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse

from schemas import PostData

from db import get_db, Session
from models import User, Post
from routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_post_page(user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    # returning all posts json here
    pass


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


@router.put("/{post_id}")
async def update_post():
    pass


@router.delete("/{post_id}")
async def delete_post():
    pass
