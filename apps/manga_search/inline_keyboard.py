from aiogram.utils.keyboard import InlineKeyboardBuilder


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
        .button(text='Буду читать', callback_data='read_now')
        .button(text='Избранное', callback_data='add_to_favorites')
        .button(text='Назад', callback_data='back_to_manga_search')
        .button(text='Выход', callback_data='delete_message')
    )
    return kb.adjust(2, 1, 1).as_markup(resize_keyboard=True)
