from aiogram.utils.keyboard import InlineKeyboardBuilder


def delete_message_kb():
    kb = InlineKeyboardBuilder()
    (
        kb
        .button(text='Скрыть', callback_data='close_message')
    )
    return kb.as_markup(resize_keyboard=True)
