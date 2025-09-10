from fastapi import APIRouter

from routers.auth.register import get_register_page, get_register
from routers.auth.login import get_login_page, get_login
from routers.auth.logout import get_logout
from routers.auth.middleware import get_current_user


import routers.auth.register as register
import routers.auth.login as login
import routers.auth.logout as logout

router = APIRouter()
router.include_router(register.router)
router.include_router(login.router)
router.include_router(logout.router)
