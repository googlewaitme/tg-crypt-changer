from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data import messages


def get_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        KeyboardButton(messages.CANCEL_BUTTON_TEXT),
        KeyboardButton(messages.CONFIRMATION_BUTTON_TEXT)
    )
    return markup
