from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.manga_search.inline_keyboard import (chapter_detailed_kb,
                                               manga_navigate_kb)
from apps.manga_search.states import MangaSearchStates
from global_objects import manga_service
from global_objects.schemas import MangaSchema
from global_objects.utils import delete_message, get_state_data

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


@router.message(MangaSearchStates.get_chapter, get_state_data)
async def manga_navigate(
    message: Message,
    state: FSMContext,
    current_manga: MangaSchema,
    core_message: Message
):
    if not message.text.isdigit():
        return
    current_chapter = await manga_service.get_chapter_by_number(current_manga.id, int(message.text))
    if not current_chapter:
        return await delete_message(await message.answer('Глава не найдена'), 5)

    await delete_message(core_message)

    mes = await message.answer(str(current_chapter), reply_markup=chapter_detailed_kb())
    await state.update_data(current_chapter=current_chapter, core_message=mes)
