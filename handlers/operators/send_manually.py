from loader import dp, get_currency, coin_api

from datetime import datetime

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from utils.db_api.models import Cashbox, User, Transaction
from states.operator_waiting import ManualTransaction
from keyboards.default import (confirmation_key,
                               back_to_menu_key)
from keyboards.operator.default import procents_key, operator_menu_key
from data import messages


@dp.message_handler(
    Text(['BTC📥', 'LTC📥']),
    is_operator=True)
async def ask_wallet_adress(message: types.Message, state: FSMContext):
    currency_name = message.text[:-1]
    markup = back_to_menu_key.get_markup()
    text = f'Введите адрес <b>{currency_name}-кошелька</b>'
    await message.answer(text, reply_markup=markup)
    await ManualTransaction.INPUT_WALLET_ADRESS.set()
    await state.update_data(currency_name=currency_name)


@dp.message_handler(state=ManualTransaction.INPUT_WALLET_ADRESS)
async def ask_count_of_currency(message: types.Message, state: FSMContext):
    text = f'Введите процентную ставку(можно ввести с клавиатуры)'
    markup = procents_key.get_markup()
    await message.answer(text, reply_markup=markup)
    await ManualTransaction.INPUT_TRANSACTION_PROCENT.set()
    await state.update_data(wallet_adress=message.text)


@dp.message_handler(
    state=ManualTransaction.INPUT_TRANSACTION_PROCENT,
    text_is_positive_int=False
)
async def send_fucking_message(message: types.Message):
    text = 'Число должно быть целым и больше или равно 0'
    await message.answer(text)


@dp.message_handler(
    state=ManualTransaction.INPUT_TRANSACTION_PROCENT,
    text_is_positive_int=True)
async def set_transaction_procent(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency_name = data['currency_name']
    text = f'Введите количество {currency_name}, которое хотите отправить'
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    await ManualTransaction.INPUT_COUNT_OF_CURRENCY.set()
    await state.update_data(procent=int(message.text))
    data = await state.get_data()


@dp.message_handler(
    state=ManualTransaction.INPUT_COUNT_OF_CURRENCY,
    text_is_float=False)
async def send_that_count_of_currency_is_float(message: types.Message):
    await message.answer(messages.INPUTING_ERROR_MESSAGE)


@dp.message_handler(
    state=ManualTransaction.INPUT_COUNT_OF_CURRENCY,
    text_is_float=True)
async def ask_confirmation_of_transaction(
        message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency_name = data['currency_name']
    wallet_adress = data['wallet_adress']

    currency = get_currency[currency_name]
    amount = float(message.text)
    currency_amount, native_amount = currency.get_amounts(amount)

    if currency_amount is None:
        text = f'(Напишите сумму : от 0.001 {currency_name} или от 300 руб)'
        await message.answer(text)
        return

    comission = currency.get_commision(native_amount, data['procent'])
    endly_native_amount = comission + native_amount
    markup = confirmation_key.get_markup()
    text = messages.OPERATOR_MANUALLY_ITOG.format(
        currency_name=currency_name,
        rub_count=endly_native_amount,
        currency_count=currency_amount,
        wallet_adress=wallet_adress,
        comission=comission)

    await message.answer(text, reply_markup=markup)
    await ManualTransaction.CONFIRMATION.set()
    await state.update_data(
        currency_count=currency_amount,
        rub_count=endly_native_amount,
        comission_count=comission,
        create_date=datetime.now()
    )


@dp.message_handler(
    Text(messages.CONFIRMATION_BUTTON_TEXT),
    state=ManualTransaction.CONFIRMATION,
    is_operator=True)
async def make_transaction(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await create_transaction(data, message)
    markup = operator_menu_key.get_markup()
    await state.finish()
    await message.answer('Меню', reply_markup=markup)


async def create_transaction(data, message):
    currency = get_currency[data['currency_name']]
    user = User.get(User.telegram_id == message.from_user.id)
    cashbox, created = Cashbox.get_or_create(closed=None)
    transaction = Transaction.create(
        user=user,
        cashbox=cashbox,
        is_operator_checked=True,
        is_paid=True,
        **data)
    coin_api.send_money(transaction=transaction, currency=currency)
