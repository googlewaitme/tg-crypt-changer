from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp, coin_api
from data import config
from states.operator_waiting import OperatorWaiting
from keyboards.default import choose_currency, operator_menu_key


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


@dp.message_handler(state=OperatorWaiting.CALCULATE_INPUT_COUNT)
async def result_of_calculating(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await ask_about_currency(message, state)
        return
    data = await state.get_data()
    await state.finish()
    count_of_rub = int(message.text)
    cur_name = data['currency']
    result = coin_api.get_coin_price(base=cur_name)
    cource_base_to_currency = float(result)
    count_of_cur = round(count_of_rub / cource_base_to_currency, 8)
    text = f"{count_of_rub} рублей = {count_of_cur} {cur_name}"
    await message.answer(text, reply_markup=operator_menu_key.get_markup())
