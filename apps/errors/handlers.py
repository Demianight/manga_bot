from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message
from peewee import DoesNotExist

from apps.errors.exceptions import RequestException
from global_objects.reply_keyboard import main_kb

router = Router()


@router.error(F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message, state: FSMContext):
    if isinstance(event.exception, RequestException):
        return await message.answer("Кажется что-то пошло не так при ответе MangaDex, возвращаю вас в главное меню.")
    if isinstance(event.exception, DoesNotExist):
        return await message.answer(
            "Пожалуйста, нажмите /start. Если это сообщение не пропадает обратитесь к @komar197"
        )

    await message.answer(
        "Что то сломалось((. Возвращаю вас в главное меню. "
        "Можете попробовать снова. Разработчики уже оповещены об ошибке.",
        reply_markup=main_kb()
    )
    await state.clear()
    raise event.exception
