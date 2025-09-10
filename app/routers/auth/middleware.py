from typing import Union
from fastapi import Request

from db import get_db
from models import User, SessionModel
from datetime import datetime, timezone


def get_current_user(request: Request) -> Union[User, None]:
    db = next(get_db())
    try:
        session_id = request.cookies.get("session")
        if not session_id:
            return None
        session = (
            db.query(SessionModel)
            .filter(
                SessionModel.session_id == session_id,
                SessionModel.expires_at > datetime.now(timezone.utc),
            )
            .first()
        )
        if not session:
            return None
        user = db.query(User).get(session.user_id)
        return user
    finally:
        db.close()
