from aiogram.fsm.context import FSMContext
from aiogram.methods import Request


async def get_state_data(_: Request, state: FSMContext):
    data = await state.get_data()
    return data
