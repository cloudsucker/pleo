import uuid
from db import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
