from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message

from global_objects.reply_keyboard import main_kb
from models import User

router = Router()


@router.error(F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message, state: FSMContext):
    user: User = User.get_or_none(message.from_user.id)
    if not user:
        return await message.answer("Не нашёл тебя в базе данных. Напиши /start и пройди регистрацию")
    await message.answer("Кажется что-то пошло не так при обработке вашего запроса, возвращаю вас в главное меню. "
                         "Разработчики уже активно работают над устранением этой проблемы и в "
                         "ближайшее время выпустят обновление",
                         reply_markup=main_kb())
    await state.clear()
    raise event.exception
