from contextlib import suppress
import logging
import os
import pickle

from aiogram import Bot, Dispatcher

from apps import last_router, main_router
from env import settings


async def start_bot(info: list[str]):
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    dp.include_routers(main_router, last_router)
    # Перезагружаем контекст
    with suppress(ValueError, IndexError):
        tg_id = int(info[1])
        await load_context_storage(bot, dp, tg_id)
    await dp.start_polling(bot)


async def load_context_storage(bot: Bot, dp: Dispatcher, tg_id: int):
    if os.path.exists('state_dump.pkl'):
        with open('state_dump.pkl', 'rb') as file:
            dp.storage.storage = pickle.load(file)
        os.remove('state_dump.pkl')
    await bot.send_message(chat_id=tg_id,
                           text="Бот успешно перезагружен!")
