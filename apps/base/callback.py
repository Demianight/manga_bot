from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from global_objects.reply_keyboard import main_kb
from global_objects.utils import delete_message

router = Router()


@router.callback_query(F.data == "delete_message")
async def _delete_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Возвращаю на главную', reply_markup=main_kb())
    await delete_message(callback.message)
    await state.clear()


@router.callback_query(F.data == "close_message")
async def _close_message(callback: CallbackQuery, state: FSMContext):
    await delete_message(callback.message)
