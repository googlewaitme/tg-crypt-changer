from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Купить BTC"), KeyboardButton("Купить LTC"))
    markup.add(
        KeyboardButton("Калькулятор цен"),
        KeyboardButton("Купим вашу крипту"))
    markup.add(KeyboardButton("Партнёрка"), KeyboardButton("Отзывы"))
    return markup
