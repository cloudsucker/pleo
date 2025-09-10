import logging
from jinja2 import Template

from db import get_db
from models import User, Post

logger = logging.getLogger(__name__)
logger.info("Loading html pages.")

PAGES_ROOT_PATH = "static/pages/"
TEMPLATES_ROOT_PATH = "static/templates/"

login_page = open(PAGES_ROOT_PATH + "login.html", "r", encoding="utf-8").read()
register_page = open(PAGES_ROOT_PATH + "register.html", "r", encoding="utf-8").read()
home_page = open(PAGES_ROOT_PATH + "home.html", "r", encoding="utf-8").read()

_account_info_template_page = open(
    TEMPLATES_ROOT_PATH + "profile.jinja2", "r", encoding="utf-8"
).read()
_posts_template_page = open(
    TEMPLATES_ROOT_PATH + "posts.jinja2", "r", encoding="utf-8"
).read()

logger.info("Html pages and templates was loaded.")


def get_post_data(post: Post):
    return {
        "id": post.id,
        "text": post.text,
        "author_username": post.author_obj.username,
        "created_at": post.created_at,
    }


def get_posts_html_page():
    db = next(get_db())
    try:
        posts = (
            db.query(Post)
            .order_by(Post.created_at.desc())
            .filter_by(deleted_at=None)
            .all()
        )
        posts_data = [get_post_data(p) for p in posts]
        return Template(_posts_template_page).render(posts=posts_data)
    finally:
        db.close()


def get_profile_html_page(user: User):
    db = next(get_db())
    try:
        user = db.query(User).filter(User.username == user.username).first()
        user.password_hash = None
        return Template(_account_info_template_page).render(user=user)
    finally:
        db.close()
