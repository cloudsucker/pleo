import uuid
import logging
from datetime import datetime, timedelta, timezone

from db import Session
from models import User, SessionModel


logger = logging.getLogger(__name__)


def create_user_session(db: Session, user: User) -> SessionModel:
    session_id = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    session = SessionModel(
        user_id=user.id, session_id=session_id, expires_at=expires_at
    )
    db.add(session)
    db.commit()

    logger.info(f"User {user.username} logged in.")

    return session
