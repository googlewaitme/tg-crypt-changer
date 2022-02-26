from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton('Приход'),
        KeyboardButton('Отправкa')
    )
    markup.row(KeyboardButton('Меню'))
    return markup
