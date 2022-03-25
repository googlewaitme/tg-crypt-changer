from loader import dp, get_currency

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards.default import choose_currency, choose_operation_type
from keyboards.default import back_to_menu_key
from keyboards.operator.default import operator_menu_key
from states.operator_waiting import OperatorWaiting


@dp.message_handler(Text('CB🎏'), is_operator=True)
async def choose_currency_handler(message: types.Message):
    text = "Выберите тип операции"
    markup = choose_operation_type.get_markup()
    await OperatorWaiting.INPUT_TYPE_OF_TRANSACTION.set()
    await message.answer(text, reply_markup=markup)


@dp.message_handler(state=OperatorWaiting.INPUT_TYPE_OF_TRANSACTION)
async def set_transaction_type(message: types.Message, state: FSMContext):
    text = "Выберите монету"
    operation_type = 'buy' if message.text == 'Приход' else 'send'
    markup = choose_currency.get_markup()
    await OperatorWaiting.INPUT_TRANSACTIONS_CURRENCY.set()
    await message.answer(text, reply_markup=markup)
    await state.update_data(operation_type=operation_type)


@dp.message_handler(state=OperatorWaiting.INPUT_TRANSACTIONS_CURRENCY)
async def set_transactions(message: types.Message, state: FSMContext):
    currency_name = message.text
    currency = get_currency[currency_name]
    data = await state.get_data()
    text = currency.get_transactions(operation_type=data['operation_type'])
    markup = operator_menu_key.get_markup()
    await message.answer(text, reply_markup=markup)
    await state.finish()
    if data['operation_type'] == 'buy':
        await ask_about_amount_of_buing(message, state, currency)


async def ask_about_amount_of_buing(message: types.Message, state, currency):
    cash_arrival = currency.get_cash_arrival_which_operator_not_checked()
    if cash_arrival is None:
        return
    amount = cash_arrival.currency_amount
    currency_name = cash_arrival.currency_name
    text = f"ВНИМАНИЕ!!!\n\nВведите количество денег, которое вы "
    text += f"заплатили за {amount} {currency_name}"
    back_to_menu = back_to_menu_key.get_markup()
    await state.update_data(
        currency_name=currency_name,
        cash_arrival_id=cash_arrival.id)
    await message.answer(text, reply_markup=back_to_menu)
    await OperatorWaiting.INPUT_COUNT_OF_PAYING.set()


@dp.message_handler(
    state=OperatorWaiting.INPUT_COUNT_OF_PAYING,
    text_is_float=False)
async def send_error(message: types.Message, state: FSMContext):
    await message.answer('Ответ должен быть числом!')


@dp.message_handler(
    state=OperatorWaiting.INPUT_COUNT_OF_PAYING, text_is_float=True)
async def write_sum_in_db(message: types.Message, state: FSMContext):
    new_native_amount = float(message.text)
    data = await state.get_data()
    currency = get_currency[data['currency_name']]
    currency.update_cash_arrival(
        data['cash_arrival_id'],
        native_amount=new_native_amount,
        is_operator_checked=True)
    menu_key = operator_menu_key.get_markup()
    await message.answer('Записано', reply_markup=menu_key)
    await state.finish()
