from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data import config


def get_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Поддержка', url=config.URL_TO_OPERATOR))
    return markup
