import logging
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from static import home_page


logger = logging.getLogger(__name__)
router = APIRouter()
users = {}


# = = = = = = = PAGE GETTERS = = = = = = = =


@router.get("/", response_class=HTMLResponse)
async def get_home_page():
    return HTMLResponse(
        home_page,
        200,
        {"Content-Type": "text/html"},
        media_type="text/html",
    )
