from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

DATABASE_URL = "postgresql+psycopg2://pleo_user:pleo_pass@pleo-db:5432/pleo-db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, Session, Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
