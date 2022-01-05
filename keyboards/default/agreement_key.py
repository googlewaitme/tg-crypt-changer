from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton('Я СОГЛАШАЮСЬ'), KeyboardButton('Я НЕ СОГЛАШАЮСЬ'))
    return markup
