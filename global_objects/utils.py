import os
from asyncio import sleep
import re

from aiogram.fsm.context import FSMContext
from aiogram.methods import Request
from aiogram.types import Message


async def get_state_data(_: Request, state: FSMContext):
    data = await state.get_data()
    return data


async def add_message_to_delete_list(mes, state: FSMContext):
    data = await state.get_data()
    messages = data.pop('messages_to_delete', [])
    messages.append(mes)
    await state.update_data(messages_to_delete=messages)


async def delete_messages(state: FSMContext):
    data = await state.get_data()
    messages: list[Message] = data.pop('messages_to_delete', [])
    for mes in messages:
        await delete_message(mes)


async def delete_message(mes: Message, delay: float = 0):
    await sleep(delay)
    await mes.delete()


def normalize_filename(filename: str):
    base, ext = os.path.splitext(filename)

    base = base.replace(" ", "_").replace('.', '')
    base = re.sub(r'[^\w\-_\.]', '', base)

    max_base_length = 255 - len(ext)
    base = base[:max_base_length]

    normalized_filename = base + ext

    return normalized_filename
