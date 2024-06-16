from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from global_objects.reply_keyboard import main_kb
from models import User

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    User.get_or_create(id=message.from_user.id)
    await message.answer(
        "Привет!\n\nЯ бот который поможет вам скачивать и читать мангу в удобном для вас формате!\n\n"
        "Надеюсь, что у нас все получиться!",
        reply_markup=main_kb(),
    )


@router.message(F.text == "Помощь")
async def help(message: Message):
    await message.answer("Господи, помогите мне, я уже не могу")


last_router = Router()


@last_router.message()
async def random_message(message: Message, state: FSMContext):
    await message.answer("Не понял о чем ты :(\nВозвращаю на главную", reply_markup=main_kb())
    await state.clear()
