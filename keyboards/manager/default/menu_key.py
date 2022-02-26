from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton('Статистика'),
        KeyboardButton('Резерв'),
        KeyboardButton('Промокоды'),
    )
    markup.row(
        KeyboardButton('Касса'),
        KeyboardButton('Конкурс'),
    )
    markup.row(
        KeyboardButton('История CB'),
        KeyboardButton('Рассылка')
    )
    return markup
