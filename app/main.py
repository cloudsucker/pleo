import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI

from app.routers import auth, post

# Reloading the pages/pages.py file
from app.static import post_page, register_page, login_page

# Logging configuration
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

# FastAPI configuration
logging.info("Starting the pleo.")
app = FastAPI()
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/post", tags=["post"])
logging.info("Pleo started.")
