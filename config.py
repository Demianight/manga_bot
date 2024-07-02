import asyncio
from contextlib import suppress
import logging
import os
import pickle

from aiogram import Bot, Dispatcher

from apps import last_router, main_router
from env import settings


def start_bot(info: list[str]):
    logging.basicConfig(level=logging.INFO)
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    with suppress(ValueError, IndexError):
        tg_id = int(info[1])
        asyncio.run(load_context_storage(bot, dp, tg_id))
    dp.include_router(main_router)
    dp.include_router(last_router)
    asyncio.run(dp.start_polling(bot))


async def load_context_storage(bot: Bot, dp: Dispatcher, tg_id: int):
    with open('state_dump.pkl', 'rb') as file:
        dp.storage.storage = pickle.load(file)

    os.remove('state_dump.pkl')
    await bot.send_message(chat_id=tg_id,
                           text="Бот успешно перезагружен!")
