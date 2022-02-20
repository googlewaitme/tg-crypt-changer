from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data import messages


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(messages.CANCEL_BUTTON_TEXT))
    return markup
