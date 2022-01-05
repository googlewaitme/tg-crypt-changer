from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data import config


def get_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Правила', url=config.URL_TO_RULES))
    return markup
