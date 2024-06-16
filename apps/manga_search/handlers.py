from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apps.manga_search.inline_keyboard import manga_navigate_kb
from apps.manga_search.states import MangaSearchStates
from global_objects import manga_service

router = Router()


@router.message(F.text == 'Поиск')
async def manga_search(message: Message, state: FSMContext):
    await message.answer('Введи название тайтла который хочешь найти')
    await state.set_state(MangaSearchStates.name)


@router.message(MangaSearchStates.name)
async def answer_manga(message: Message, state: FSMContext):
    mangas = await manga_service.get_manga(message.text)
    await state.update_data(mangas=mangas)
    await message.answer(
        'Найденные тайтлы:\n\n' + '\n'.join([f'{i}. ' + str(manga) for i, manga in enumerate(mangas, start=1)]),
        reply_markup=manga_navigate_kb(mangas),
    )
