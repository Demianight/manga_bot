from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from apps.manga_search.inline_keyboard import (agree_kb, chapter_detailed_kb,
                                               manga_navigate_kb)
from apps.manga_search.states import MangaSearchStates
from apps.manga_search.utils import define_action, get_action_arguments, get_chapters_by_numbers
from global_objects import MangaService
from global_objects.schemas import ChapterActions, MangaSchema
from global_objects.utils import delete_message, get_state_data

router = Router()


@router.message(F.text == 'Поиск')
async def manga_search(message: Message, state: FSMContext):
    await message.answer('Введи название тайтла который хочешь найти')
    await state.set_state(MangaSearchStates.name)


@router.message(MangaSearchStates.name)
async def answer_manga(message: Message, state: FSMContext):
    async with MangaService() as client:
        mangas = await client.get_manga(message.text)
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
    action = define_action(message.text)
    if not action:
        return
    arguments = get_action_arguments(message.text, action)
    chapters, errors = await get_chapters_by_numbers(current_manga.id, arguments)
    await state.update_data(
        action=action,
        arguments=arguments,
        chapters=chapters,
        request_text=message.text,
        errors=errors
    )
    match action:
        case ChapterActions.SOLO:
            current_chapter = chapters[0]
            if not current_chapter:
                return await delete_message(await message.answer('Глава не найдена'), 5)
            await delete_message(core_message)

            mes = await message.answer(str(current_chapter), reply_markup=chapter_detailed_kb())
            await state.update_data(current_chapter=current_chapter, core_message=mes)
        case ChapterActions.RANGE:
            await message.answer(
                f'Вы точно уверены что хотите скачать главы с {arguments[0]} по {arguments[-1]}?',
                reply_markup=agree_kb(),
            )
        case ChapterActions.LIST:
            await message.answer(
                f'Вы точно уверены что хотите скачать главы {", ".join(map(str, arguments))}?',
                reply_markup=agree_kb(),
            )
