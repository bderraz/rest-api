from fastapi.routing import APIRouter

from tvshow_backend.web.api import docs, echo, monitoring, tvshow

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(tvshow.router, prefix="/tvshow", tags=["tvshow"])
