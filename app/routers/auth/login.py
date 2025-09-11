from passlib.hash import bcrypt
from fastapi import APIRouter, Response, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, HTMLResponse

from db import get_db, Session
from models import User
from static import login_page
from schemas import UserPassword
from routers.auth._create_user_session import create_user_session


router = APIRouter()


@router.get("/login")
async def get_login_page():
    return HTMLResponse(login_page, 200, media_type="text/html")


@router.post("/login")
async def get_login(
    login_data: UserPassword, response: Response, db: Session = Depends(get_db)
):
    user: User = db.query(User).filter(User.username == login_data.username).first()

    if not user or not bcrypt.verify(login_data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials.")

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
