from aiogram.utils.keyboard import InlineKeyboardBuilder

from global_objects.schemas import ChapterSchema


def manga_navigate_kb(mangas: list):
    kb = InlineKeyboardBuilder()
    [kb.button(text=f'{i}', callback_data=f'manga_{i}') for i in range(1, len(mangas) + 1)]
    (
        kb
        .button(text='<<', callback_data='prev_page')
        .button(text='Выход', callback_data='delete_message')
        .button(text='>>', callback_data='next_page')
    )

    return kb.adjust(len(mangas), 3).as_markup(resize_keyboard=True)


def detailed_manga_kb():
    kb = InlineKeyboardBuilder()
    (
        kb
        .button(text='Главы', callback_data='chapters')
        # .button(text='Буду читать', callback_data='read_now')
        # .button(text='Избранное', callback_data='add_to_favorites')
        .button(text='Назад', callback_data='back_to_manga_search')
        .button(text='Выход', callback_data='delete_message')
    )
    return kb.adjust(1, 1, 1).as_markup(resize_keyboard=True)


def choose_chapter_kb(chapters: list[ChapterSchema], page: int = 0):
    kb = InlineKeyboardBuilder()
    [kb.button(text=f'{chapter.chapter}. {chapter.title}', callback_data=f'chapter_{i}')
     for i, chapter in enumerate(chapters, start=1 + (page * 5))]
    (kb
     .button(text='<<', callback_data='prev_chapters')
     .button(text='Назад', callback_data='back_to_manga_search')
     .button(text='>>', callback_data='next_chapters')
     .button(text='Выход', callback_data='delete_message'))
    return kb.adjust(*([1]*len(chapters)), 3, 1).as_markup(resize_keyboard=True)


def chapter_detailed_kb():
    kb = InlineKeyboardBuilder()
    (
        kb
        .button(text='Скачать', callback_data='download_chapter')
        .button(text='Назад', callback_data='back_to_chapters')
        .button(text='Выход', callback_data='delete_message')
    )

    return kb.adjust(1, 2).as_markup(resize_keyboard=True)
