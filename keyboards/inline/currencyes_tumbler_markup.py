from data.config import states, CURRENCYES

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


tumbler_cb = CallbackData('tumbler_currency', 'currency_name', 'in_work')


def get_markup():
    markup = InlineKeyboardMarkup(row_width=4)

    all_turn_on = tumbler_cb.new('all', in_work=True)
    markup.add(InlineKeyboardButton('Включить все', callback_data=all_turn_on))
    for currency in CURRENCYES:
        currency_in_work = currency in states['currency_in_work']
        text = currency + ("🟩" if currency_in_work else "🟥")
        callback_data = tumbler_cb.new(currency, in_work=currency_in_work)
        markup.row(InlineKeyboardButton(text, callback_data=callback_data))
    all_turn_off = tumbler_cb.new('all', in_work=False)
    markup.add(InlineKeyboardButton(
        'Выключить все', callback_data=all_turn_off))
    return markup
