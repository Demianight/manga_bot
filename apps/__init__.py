from .manga_search import router as manga_search_router
from aiogram import Router
from .errors import router as errors_router
from .base import router as base_router
from .base import last_router as last_router


__all__ = ("main_router", "last_router")


main_router = Router()

main_router.include_router(base_router)
main_router.include_router(errors_router)
main_router.include_router(manga_search_router)