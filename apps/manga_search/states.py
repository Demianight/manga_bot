from aiogram.fsm.state import State, StatesGroup


class MangaSearchStates(StatesGroup):
    name = State()
