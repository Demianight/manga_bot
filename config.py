from contextlib import suppress

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
        await bot.send_message(
            chat_id=tg_id,
            text="Бот успешно перезагружен!"
        )

    await dp.start_polling(bot)
