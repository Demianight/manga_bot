import asyncio
import logging

from aiogram import Bot, Dispatcher

from env import settings
from apps import main_router, last_router


def start_bot():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.include_router(last_router)
    asyncio.run(dp.start_polling(bot))
