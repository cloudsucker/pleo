from passlib.hash import bcrypt
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException

from db import get_db, Session
from models import User
from static import register_page
from schemas import UserPassword
from routers.auth._create_user_session import create_user_session


router = APIRouter()


@router.get("/register")
async def get_register_page():
    return HTMLResponse(register_page, 200, media_type="text/html")


@router.post("/register")
async def get_register(
    register_data: UserPassword, response: JSONResponse, db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User).filter(User.username == register_data.username).first()
    )
    if existing_user:
        raise HTTPException(401, "Username already taken.")

    hash_pass = bcrypt.hash(register_data.password)

    user = User(username=register_data.username, password_hash=hash_pass)

    db.add(user)
    db.commit()
    db.refresh(user)

    response = JSONResponse(
        content={
            "user_id": user.id,
            "username": user.username,
            "avatar": user.avatar,
            "status": 200,
        }
    )

    response.set_cookie(
        key="session",
        value=create_user_session(db, user).session_id,
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=False,
    )

    return response
