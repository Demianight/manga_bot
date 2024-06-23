import os
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from env import settings
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


@router.message(Command('stats'))
async def stats(message: Message, state: FSMContext):
    if message.from_user.id not in settings.admin_ids:
        return await random_message(message, state)

    users_count = User.select().count()
    chapters_count = len(os.listdir(settings.base_dir / 'pdfs'))
    await message.answer(
        f"Всего пользователей: {users_count}\n"
        f"Скачано глав: {chapters_count}\n"
    )

last_router = Router()


@last_router.message()
async def random_message(message: Message, state: FSMContext):
    await message.answer("Не понял о чем ты :(\nВозвращаю на главную", reply_markup=main_kb())
    await state.clear()
