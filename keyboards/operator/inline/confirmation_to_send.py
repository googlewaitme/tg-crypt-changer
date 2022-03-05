from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


user_transaction_cb = CallbackData(
    'user_transaction', 'transaction_id', 'confirmation')


def get_markup(transaction_id: int):
    markup = InlineKeyboardMarkup()
    yes_call = user_transaction_cb.new(
        transaction_id=transaction_id,
        confirmation=True)
    no_callback = user_transaction_cb.new(
        transaction_id=transaction_id,
        confirmation=False)
    markup.add(InlineKeyboardButton('🟩Подтверждаю🟩', callback_data=yes_call))
    markup.add(InlineKeyboardButton('❗Отказ❗', callback_data=no_callback))
    return markup
