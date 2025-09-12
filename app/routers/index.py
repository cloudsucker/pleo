import logging
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse


from models import User
from static import get_home_html_page
from routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()
users = {}


# = = = = = = = PAGE GETTERS = = = = = = = =


@router.get("/", response_class=HTMLResponse)
async def get_home_page(user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)

    return get_home_html_page(user)
