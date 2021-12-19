from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('BTC'), KeyboardButton('LTC'))
    markup.add(KeyboardButton("Меню"))
    return markup
