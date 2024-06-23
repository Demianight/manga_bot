from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from apps.manga_search.inline_keyboard import chapter_detailed_kb, choose_chapter_kb, detailed_manga_kb, manga_navigate_kb
from apps.manga_search.states import MangaSearchStates
from apps.manga_search.utils import get_chapters_message
from global_objects.schemas import ChapterSchema, MangaSchema
from global_objects.utils import get_state_data
from global_objects import manga_service

router = Router()


@router.callback_query(F.data.startswith("manga_"), get_state_data)
async def manga_navigate(callback: CallbackQuery, state: FSMContext, mangas: list[MangaSchema]):
    current_manga = mangas[int(callback.data[6:]) - 1]
    await state.update_data(current_manga=current_manga)
    await callback.message.edit_text(format(current_manga, 'detailed'), reply_markup=detailed_manga_kb())


@router.callback_query(F.data == 'back_to_manga_search', get_state_data)
async def back_to_manga_search(
    callback: CallbackQuery, state: FSMContext, mangas: list[MangaSchema]
):
    await callback.message.answer(
        'Найденные тайтлы:\n\n' + '\n'.join([f'{i}. ' + str(manga) for i, manga in enumerate(mangas, start=1)]),
        reply_markup=manga_navigate_kb(mangas),
    )
    await callback.message.delete()
    await state.set_state(None)


@router.callback_query(F.data == 'chapters', get_state_data)
async def chapter_navigate(
    callback: CallbackQuery, state: FSMContext, current_manga: MangaSchema
):
    chapters = await manga_service.get_chapters(current_manga.id)
    await state.update_data(page=0, chapters=chapters, core_message=callback.message)
    await callback.message.edit_text(
        get_chapters_message(chapters),
        reply_markup=choose_chapter_kb(chapters),
    )
    await state.set_state(MangaSearchStates.get_chapter)


@router.callback_query(F.data.startswith("chapter_"), get_state_data)
async def chapter_detailed(callback: CallbackQuery, state: FSMContext, chapters: list[ChapterSchema]):
    current_chapter = chapters[(int(callback.data[8:]) - 1) % 5]
    await state.update_data(current_chapter=current_chapter)
    await callback.message.edit_text(str(current_chapter), reply_markup=chapter_detailed_kb())


@router.callback_query(F.data == 'back_to_chapters', get_state_data)
async def back_to_chapters(
    callback: CallbackQuery, state: FSMContext, chapters: list[ChapterSchema], page: int, current_manga: MangaSchema
):
    chapters = await manga_service.get_chapters(current_manga.id, page * 5)
    await callback.message.edit_text(
        get_chapters_message(chapters),
        reply_markup=choose_chapter_kb(chapters, page),
    )


@router.callback_query(F.data == 'download_chapter', get_state_data)
async def download_chapter(callback: CallbackQuery, state: FSMContext, current_chapter: ChapterSchema):
    mes = await callback.message.answer('Скачиваю...')
    file_path = await manga_service.download_chapter(current_chapter.id)
    await mes.delete()
    mes = await callback.message.answer('Обрабатываю...')
    input_file = FSInputFile(file_path, f'{current_chapter.title}.pdf')
    await mes.delete()
    mes = await callback.message.answer('Отправляю...')
    await callback.message.answer_document(input_file)
    await mes.delete()


@router.callback_query(F.data == 'next_chapters', get_state_data)
async def next_chapters(callback: CallbackQuery, state: FSMContext, page: int, current_manga: MangaSchema):
    chapters = await manga_service.get_chapters(current_manga.id, (page + 1) * 5)
    await state.update_data(page=page + 1, chapters=chapters)
    await callback.message.edit_text(
        get_chapters_message(chapters),
        reply_markup=choose_chapter_kb(chapters, page + 1),
    )


@router.callback_query(F.data == 'prev_chapters', get_state_data)
async def prev_chapters(callback: CallbackQuery, state: FSMContext, page: int, current_manga: MangaSchema):
    if page == 0:
        return await callback.answer('Это первая страница')
    chapters = await manga_service.get_chapters(current_manga.id, (page - 1) * 5)
    await state.update_data(page=page - 1, chapters=chapters)
    await callback.message.edit_text(
        get_chapters_message(chapters),
        reply_markup=choose_chapter_kb(chapters, page - 1),
    )
