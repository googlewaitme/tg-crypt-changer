from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, currencyes
from data import config, messages
from states.operator_waiting import OperatorWaiting
from keyboards.default import choose_currency
from keyboards.operator.default import operator_menu_key


@dp.message_handler(Text(startswith='🧮'), is_operator=True)
async def ask_about_currency(message: types.Message, state: FSMContext):
    await OperatorWaiting.CALCULATE_CHOOSE_CURRENCY.set()
    text = 'Выбор валюты:'
    markup = choose_currency.get_markup()
    await message.answer(text, reply_markup=markup)


@dp.message_handler(state=OperatorWaiting.CALCULATE_CHOOSE_CURRENCY)
async def ask_about_count(message: types.Message, state: FSMContext):
    if message.text not in config.CURRENCYES:
        text = "<b>Неверный ввод:</b> "
        await message.answer(text)
        text = f"Возможные варианты: {', '.join(config.CURRENCYES)}"
        await message.answer(text)
        return
    text = f"Ввод значения для <b>{message.text}</b> в рублях"
    markup = types.ReplyKeyboardRemove()
    await message.answer(text, reply_markup=markup)
    await state.update_data(currency=message.text)
    await OperatorWaiting.CALCULATE_INPUT_COUNT.set()


@dp.message_handler(
    text_is_float=False,
    state=OperatorWaiting.CALCULATE_INPUT_COUNT)
async def error_of_calculating(message: types.Message):
    await message.answer(messages.INPUTING_ERROR_MESSAGE)


@dp.message_handler(
    text_is_float=True,
    state=OperatorWaiting.CALCULATE_INPUT_COUNT)
async def result_of_calculating(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    amount = float(message.text)
    for cur in currencyes:
        if cur.name == data['currency']:
            currency = cur
            break
    currency_amount, native_amount = currency.get_amounts(amount)
    commission = currency.get_commision(native_amount)
    endly_native_amount = native_amount + commission
    text = f"{endly_native_amount} рублей = {currency_amount} {cur.name}\n"
    text += f"Коммиссия - {commission}, себестоимость - {native_amount}"
    await message.answer(text, reply_markup=operator_menu_key.get_markup())
