import logging
from jinja2 import Template

from db import get_db
from schemas import PostDTO, UserDTO
from models import User, Post

logger = logging.getLogger(__name__)
logger.info("Loading html pages.")

PAGES_ROOT_PATH = "static/pages/"
TEMPLATES_ROOT_PATH = "static/templates/"

login_page = open(PAGES_ROOT_PATH + "login.html", "r", encoding="utf-8").read()
register_page = open(PAGES_ROOT_PATH + "register.html", "r", encoding="utf-8").read()
home_page = open(PAGES_ROOT_PATH + "home.html", "r", encoding="utf-8").read()

_post_block_template_page = open(
    TEMPLATES_ROOT_PATH + "_post_block.jinja2", "r", encoding="utf-8"
).read()
_header_template_page = open(
    TEMPLATES_ROOT_PATH + "header.jinja2", "r", encoding="utf-8"
).read()
_account_info_template_page = open(
    TEMPLATES_ROOT_PATH + "profile.jinja2", "r", encoding="utf-8"
).read()
_wall_template_page = open(
    TEMPLATES_ROOT_PATH + "wall.jinja2", "r", encoding="utf-8"
).read()

logger.info("Html pages and templates was loaded.")


def get_wall_html_page(current_user: User):
    db = next(get_db())
    try:
        posts = (
            db.query(Post)
            .order_by(Post.created_at.desc())
            .filter_by(deleted_at=None)
            .all()
        )
        posts_dto_list = [PostDTO.from_db(p) for p in posts]

        post_template = Template(_post_block_template_page)
        rendered_posts = post_template.render(
            posts=posts_dto_list, current_user_id=current_user.id
        )

        wall_template = Template(_wall_template_page)
        return wall_template.render(
            posts_html=rendered_posts, current_user_id=current_user.id
        )
    finally:
        db.close()


def get_profile_html_page(user: User):
    db = next(get_db())
    try:
        user = db.query(User).filter(User.username == user.username).first()
        user_dto = UserDTO.from_db(user)

        header_fragment = Template(_header_template_page).render(user=user_dto)
        return Template(_account_info_template_page).render(
            user=user_dto, header_fragment=header_fragment
        )
    finally:
        db.close()
