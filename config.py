import asyncio
import logging

from aiogram import Bot, Dispatcher

from apps import last_router, main_router
from env import settings


def start_bot():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.include_router(last_router)
    asyncio.run(dp.start_polling(bot))
