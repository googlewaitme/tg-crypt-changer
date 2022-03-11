from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, get_currency
from data import config
from states.user_waiting import UserWaiting
from keyboards.default import choose_currency, menu_key


@dp.message_handler(Text(startswith='Калькулятор'))
async def ask_about_currency(message: types.Message, state: FSMContext):
    await UserWaiting.CALCULATE_CHOOSE_CURRENCY.set()
    text = 'Выбор валюты:'
    markup = choose_currency.get_markup()
    await message.answer(text, reply_markup=markup)


@dp.message_handler(state=UserWaiting.CALCULATE_CHOOSE_CURRENCY)
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
    await state.update_data(currency_name=message.text)
    await UserWaiting.CALCULATE_INPUT_COUNT.set()


@dp.message_handler(state=UserWaiting.CALCULATE_INPUT_COUNT)
async def result_of_calculating(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await ask_about_currency(message, state)
        return
    data = await state.get_data()
    currency_name = data['currency_name']
    currency = get_currency[currency_name]
    amount = float(message.text)
    currency_amount, native_amount = currency.get_amounts(amount)

    if currency_amount is None:
        text = f'(Напишите сумму : от 0.001 {currency_name} или от 300 руб)'
        await message.answer(text)
        return

    commission = currency.get_commision(native_amount)
    text = f"{native_amount + commission} рублей ="
    text += f" {currency_amount} {currency_name}"
    text += f'\nКоммисия: {commission}'
    await message.answer(text, reply_markup=menu_key.get_markup())
    await state.finish()
