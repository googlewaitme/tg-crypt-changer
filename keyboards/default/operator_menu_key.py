from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton('СВ'),
        KeyboardButton('BTC📥'),
        KeyboardButton('LTC📥'),
        KeyboardButton('СВ🎏'),
    )
    markup.row(
        KeyboardButton('🧮'),
        KeyboardButton('💳'),
    )
    markup.row(
        KeyboardButton('🕹️'),
        KeyboardButton('Бан'),
        KeyboardButton('Резерв'),
    )
    return markup
