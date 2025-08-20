import logging

logger = logging.getLogger(__name__)
logger.info("Loading html pages.")

login_page = open("static/pages/login.html", "r", encoding="utf-8").read()
register_page = open("static/pages/register.html", "r", encoding="utf-8").read()
posts_page = open("static/pages/posts.html", "r", encoding="utf-8").read()

logger.info("Html pages was loaded.")
