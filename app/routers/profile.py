import logging
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from static import get_profile_html_page
from routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_profile_page(user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=401)

    html_content = get_profile_html_page(user)
    return HTMLResponse(html_content)
