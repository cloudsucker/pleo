from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from db import get_db
from models import SessionModel


router = APIRouter()


@router.post("/logout")
async def get_logout(request: Request, response: Response):
    db = next(get_db())
    try:
        session_id = request.cookies.get("session")
        if session_id:
            db.query(SessionModel).filter(
                SessionModel.session_id == session_id
            ).delete()
            db.commit()
        response = JSONResponse({"status": 200}, status_code=200)
        response.delete_cookie("session")
        return response
    finally:
        db.close()
