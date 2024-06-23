from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apps.manga_search.inline_keyboard import choose_chapter_kb, manga_navigate_kb
from apps.manga_search.states import MangaSearchStates
from apps.manga_search.utils import get_chapters_message
from global_objects import manga_service
from global_objects.schemas import MangaSchema
from global_objects.utils import get_state_data

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
    await core_message.delete()
    page = int(message.text) // 5
    chapters = await manga_service.get_chapters(current_manga.id, page * 5)
    mes = await message.answer(
        get_chapters_message(chapters),
        reply_markup=choose_chapter_kb(chapters, page),
    )
    await state.update_data(page=page, chapters=chapters, core_message=mes)
