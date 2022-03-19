from loader import dp, get_currency

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards.default import choose_currency, choose_operation_type
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
