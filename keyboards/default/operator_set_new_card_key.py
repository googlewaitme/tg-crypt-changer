from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Меню'), KeyboardButton('Загрузить карту'))
    return markup
