from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton('CB'),
        KeyboardButton('BTC📥'),
        KeyboardButton('LTC📥'),
        KeyboardButton('CB🎏'),
    )
    markup.row(
        KeyboardButton('🧮'),
        KeyboardButton('💳'),
        KeyboardButton('Процент📌')
    )
    markup.row(
        KeyboardButton('🕹️'),
        KeyboardButton('Бан'),
        KeyboardButton('Резерв'),
    )
    return markup
