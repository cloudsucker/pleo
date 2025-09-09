import bcrypt
import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException

from app.models import UserPassword
from app.static import register_page, login_page


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
    hash_pass = bcrypt.hashpw(register_data.password.encode("utf-8"), bcrypt.gensalt())

    users[register_data.username] = hash_pass

    logger.info(f"Registering new user: {register_data.username}.")

    return JSONResponse(
        {
            "message": f"Hello, {register_data.username}! You are registered.",
            "status": 200,
        },
        200,
        {"Content-Type": "application/json"},
        media_type="application/json",
    )


@router.post("/login")
async def login(login_data: UserPassword):
    hash_pass = users.get(login_data.username, None)

    if not hash_pass or not bcrypt.checkpw(
        login_data.password.encode("utf-8"), hash_pass
    ):
        logger.info(f"User {login_data.username} is trying to login.")
        raise HTTPException(401, "Invalid credentials.")

    logger.info(f"User {login_data.username} logged in.")
    return JSONResponse(
        {
            "message": f"Hello, {login_data.username}! You are logged in.",
            "status": 200,
        },
        200,
        {"Content-Type": "application/json"},
        media_type="application/json",
    )
