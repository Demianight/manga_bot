from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message

from apps.errors.exceptions import RequestException
from global_objects.reply_keyboard import main_kb

router = Router()


@router.error(F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message, state: FSMContext):
    if isinstance(event.exception, RequestException):
        return await message.answer("Кажется что-то пошло не так при ответе MangaDex, возвращаю вас в главное меню.")

    await message.answer(
        "Кажется что-то пошло не так при обработке вашего запроса, возвращаю вас в главное меню. "
        "Разработчики уже активно работают над устранением этой проблемы и в "
        "ближайшее время выпустят обновление",
        reply_markup=main_kb()
    )
    await state.clear()
    raise event.exception
