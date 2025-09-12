import logging
from passlib.hash import bcrypt
from datetime import timezone, datetime
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Body, Depends


from models import User
from schemas import UserDTO
from db import get_db, Session
from routers.auth import get_current_user


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/{user_id}")
async def get_user(
    user_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    if not user:
        return JSONResponse({"message": "Unauthorized", "status": 401})

    founded_user = db.query(User).filter(User.id == user_id).first()
    if not founded_user:
        return JSONResponse({"message": "User not found", "status": 404})

    return UserDTO.from_db(founded_user)


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_update: dict = Body(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if user.id != user_id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to update this user."
        )

    founded_user = db.query(User).filter(User.id == user_id).first()
    if not founded_user:
        raise HTTPException(status_code=404, detail="User not found")

    # avatar change
    if "avatar" in user_update:
        founded_user.avatar = user_update["avatar"]

    # username change
    if "username" in user_update:
        new_username = user_update.get("username")
        if new_username and new_username != founded_user.username:
            existing = db.query(User).filter(User.username == new_username).first()
            if existing and existing.id != founded_user.id:
                raise HTTPException(status_code=409, detail="Username already taken")
            founded_user.username = new_username

    # password change
    old_password = user_update.get("old_password")
    new_password = user_update.get("new_password")
    if old_password and new_password:
        if not bcrypt.verify(old_password, founded_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials.")
        founded_user.password_hash = bcrypt.hash(new_password)

    db.commit()
    db.refresh(founded_user)

    response = UserDTO.from_db(founded_user).model_dump()
    response["status"] = 200
    return response


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return JSONResponse({"message": "Unauthorized", "status": 401})

    if user.id != user_id:
        return JSONResponse(
            {"message": "You are not allowed to delete this user.", "status": 403}
        )

    founded_user = db.query(User).filter(User.id == user_id).first()
    if not founded_user:
        return JSONResponse({"message": "User not found", "status": 404})

    founded_user.deleted_at = datetime.now(timezone.utc)
    db.commit()

    return JSONResponse(
        {
            "user_id": founded_user.id,
            "message": "User deleted successfully",
            "status": 200,
        }
    )
