import logging
from passlib.hash import bcrypt
from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException

from schemas import UserPassword
from static import register_page, login_page

from db import SessionLocal
from models import User


logger = logging.getLogger(__name__)
router = APIRouter()
users = {}


# = = = = = = = PAGE GETTERS = = = = = = = =


@router.get("/register")
async def get_register_page():
    return HTMLResponse(
        register_page,
        200,
        {"Content-Type": "text/html"},
        media_type="text/html",
    )


@router.get("/login")
async def get_login_page():
    return HTMLResponse(
        login_page,
        200,
        {"Content-Type": "text/html"},
        media_type="text/html",
    )


# = = = = = = = DATA POST ENDPOINTS = = = = = = = =


@router.post("/register")
async def register(register_data: UserPassword):
    db = SessionLocal()

    try:
        existing_user = (
            db.query(User).filter(User.username == register_data.username).first()
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hash_pass = bcrypt.hash(register_data.password)

        logger.info(f"Registering new user: {register_data.username}.")
        user = User(username=register_data.username, password_hash=hash_pass)

        db.add(user)
        db.commit()
        db.refresh(user)

        return JSONResponse(
            {"user_id": user.id, "username": user.username, "status": 200},
            status_code=200,
        )
    finally:
        db.close()


@router.post("/login")
async def login(login_data: UserPassword):
    db = SessionLocal()

    try:
        existing_user = (
            db.query(User).filter(User.username == login_data.username).first()
        )
        if not existing_user:
            raise HTTPException(401, "Invalid credentials.")

        if not bcrypt.verify(login_data.password, existing_user.password_hash):
            logger.info(f"User {login_data.username} is trying to login.")
            raise HTTPException(401, "Invalid credentials.")

        logger.info(f"User {login_data.username} logged in.")
        return JSONResponse(
            {
                "user_id": existing_user.id,
                "username": existing_user.username,
                "status": 200,
            },
            200,
            {"Content-Type": "application/json"},
            media_type="application/json",
        )
    finally:
        db.close()
