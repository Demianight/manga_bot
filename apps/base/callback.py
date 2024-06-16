from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from global_objects.reply_keyboard import main_kb

router = Router()


@router.callback_query(F.data == "delete_message")
async def delete_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Возвращаю на главную', reply_markup=main_kb())
    await callback.message.delete()
    await state.clear()
