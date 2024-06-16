from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from apps.manga_search.inline_keyboard import detailed_manga_kb, manga_navigate_kb
from global_objects.schemas import MangaSchema
from global_objects.utils import get_state_data

router = Router()


@router.callback_query(F.data.startswith("manga_"), get_state_data)
async def manga_navigate(callback: CallbackQuery, state: FSMContext, mangas: list[MangaSchema]):
    current_manga = mangas[int(callback.data[6:]) - 1]
    await callback.message.edit_text(format(current_manga, 'detailed'), reply_markup=detailed_manga_kb())


@ router.callback_query(F.data == 'back_to_manga_search', get_state_data)
async def back_to_manga_search(
    callback: CallbackQuery, state: FSMContext, mangas: list[MangaSchema]
):
    await callback.message.answer(
        'Найденные тайтлы:\n\n' + '\n'.join([f'{i}. ' + str(manga) for i, manga in enumerate(mangas, start=1)]),
        reply_markup=manga_navigate_kb(mangas),
    )
    await callback.message.delete()
