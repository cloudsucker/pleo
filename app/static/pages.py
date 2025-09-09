import logging

logger = logging.getLogger(__name__)
logger.info("Loading html pages.")

login_page = open("app/static/pages/login.html", "r", encoding="utf-8").read()
register_page = open("app/static/pages/register.html", "r", encoding="utf-8").read()
post_page = open("app/static/pages/post.html", "r", encoding="utf-8").read()

logger.info("Html pages was loaded.")
