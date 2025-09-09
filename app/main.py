import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI

from routers import auth, post, index

# Reloading the pages/pages.py file
from static import post_page, register_page, login_page

from db import Base, engine
from models import User, Post

# Database Initialization
Base.metadata.create_all(bind=engine)

# = = = = = = = Logging configuration = = = = = = = = = =

log_handler = RotatingFileHandler(
    "app.log", maxBytes=5 * 1024 * 1024, backupCount=5  # 5 MB + 5 файлов ротации
)
log_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logging.getLogger("watchfiles").setLevel(logging.WARNING)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# FastAPI configuration
logging.info("Starting the pleo.")

app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/post", tags=["post"])
app.include_router(index.router, prefix="", tags=["index"])

logging.info("Pleo started.")
