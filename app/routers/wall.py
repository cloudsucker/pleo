import logging
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from static import get_wall_html_page
from routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_wall_page(user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/auth/login", status_code=302)
    html_content = get_wall_html_page()
    return HTMLResponse(html_content)
