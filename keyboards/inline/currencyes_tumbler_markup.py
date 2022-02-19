from data.config import states, CURRENCYES

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


tumbler_cb = CallbackData('tumbler_currency', 'currency_name', 'in_work')


def get_markup():
    markup = InlineKeyboardMarkup(row_width=4)
    for currency in CURRENCYES:
        currency_in_work = currency in states['currency_in_work']
        text = currency + ("🟩" if currency_in_work else "🟥")
        callback_data = tumbler_cb.new(currency, in_work=currency_in_work)
        markup.insert(InlineKeyboardButton(text, callback_data=callback_data))
    return markup
