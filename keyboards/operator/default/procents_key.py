from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=6)
    for procent in range(0, 24, 2):
        markup.insert(KeyboardButton(procent))
    return markup
