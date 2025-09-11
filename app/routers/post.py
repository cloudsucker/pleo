import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse

from schemas import PostContent, PostDTO

from db import get_db, Session
from models import User, Post
from routers.auth import get_current_user


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_all_posts(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    posts = db.query(Post).filter(Post.deleted_at == None).all()
    return [PostDTO.from_db(p) for p in posts]


@router.post("/")
async def add_post(
    post_content: PostContent,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=401)

    post = Post(author_id=user.id, text=post_content.text)
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


@router.get("/{post_id}")
async def get_post(
    post_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return JSONResponse(
            {"message": "Post not found", "status": 404}, media_type="application/json"
        )

    return PostDTO.from_db(post)


@router.put("/{post_id}")
async def update_post(
    post_id: int,
    post_content: PostContent,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    post = db.query(Post).filter(Post.id == post_id).update({"text": post_content.text})
    if not post:
        return JSONResponse(
            {"message": "Post not found", "status": 404}, media_type="application/json"
        )

    db.commit()
    db.refresh(post)

    return JSONResponse(
        {
            "post_id": post.id,
            "message": "Post updated successfully",
            "status": 200,
        },
        media_type="application/json",
    )


@router.delete("/{post_id}")
async def delete_post(
    post_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    post = db.query(Post).filter(Post.id == post_id).update({"deleted_at": None})
    if not post:
        return JSONResponse(
            {"message": "Post not found", "status": 404}, media_type="application/json"
        )

    db.commit()
    db.refresh(post)

    return JSONResponse(
        {
            "post_id": post.id,
            "message": "Post deleted successfully",
            "status": 200,
        },
        media_type="application/json",
    )
