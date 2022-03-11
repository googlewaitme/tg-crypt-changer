from loader import dp, coin_api, get_currency

from aiogram import types

from utils.db_api.models import Transaction
from keyboards.operator.inline.confirmation_to_send import user_transaction_cb
from data import messages


@dp.callback_query_handler(user_transaction_cb.filter(confirmation='True'))
async def send_money(query: types.CallbackQuery, callback_data: dict):
    """
    Оператор подтверждает перевод по заявке от пользователя
    """
    transaction = Transaction.get(id=callback_data['transaction_id'])
    user_id = transaction.user.telegram_id
    transaction.is_operator_checked = True
    transaction.save()
    text = messages.TRANSACTION_IS_PASSED
    currency = get_currency[transaction.currency_name]
    coin_api.send_money(transaction=transaction, currency=currency)
    await query.message.edit_reply_markup(types.InlineKeyboardMarkup())
    await query.message.answer('Перевод совершён!')
    await alert_to_user(user_id, text)
    await query.answer()


@dp.callback_query_handler(user_transaction_cb.filter(confirmation='False'))
async def send_refusal(query: types.CallbackQuery, callback_data: dict):
    """
    Оператор отказывает в заявке
    """
    transaction = Transaction.get(id=callback_data['transaction_id'])
    transaction.delete_instance()
    user_id = transaction.user.telegram_id
    text = messages.TRANSACTION_IS_CANCELED
    await query.message.edit_reply_markup(types.InlineKeyboardMarkup())
    await query.message.answer('Перевод отменён!')
    await alert_to_user(user_id, text)


async def alert_to_user(user_id, text):
    await dp.bot.send_message(chat_id=user_id, text=text)
