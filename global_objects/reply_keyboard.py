from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Поиск').button(text='Избранное').button(text='Помощь')
    return kb.adjust(1).as_markup(resize_keyboard=True)
