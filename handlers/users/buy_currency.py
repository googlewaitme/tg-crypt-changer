from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from datetime import datetime
import asyncio
from math import ceil
import uuid

from data import messages, config
from loader import dp, coin_api
from states.user_waiting import UserWaiting
from keyboards.default import (agreement_key, back_to_menu_key,
                               payed_or_not_key, menu_key)
from keyboards.inline import button_to_rules, button_to_support


async def send_error_message(message: types.Message, old_text: str):
    text = messages.INPUTING_ERROR_MESSAGE
    await message.answer(text)
    await message.answer(old_text)


@dp.message_handler(Text(['Купить LTC', 'Купить BTC']))
async def send_agreement(message: types.Message, state: FSMContext):
    currency_name = message.text.split()[1]
    if currency_name not in config.states['currency_in_work']:
        markup = button_to_support.get_markup()
        await message.answer(messages.CURRENCY_NOT_IN_WORK)
        return
    markup = agreement_key.get_markup()
    await message.answer(messages.AGREEMENT, reply_markup=markup)
    await state.update_data(currency_name=currency_name)
    await UserWaiting.INPUT_AGREEMENT.set()


@dp.message_handler(Text('Я СОГЛАШАЮСЬ'), state=UserWaiting.INPUT_AGREEMENT)
async def send_offer(message: types.Message, state: FSMContext):
    markup = back_to_menu_key.get_markup()
    data = await state.get_data()
    currency_name = data['currency_name']
    text = messages.OFFER_TEMPLATE.format(currency_name=currency_name)
    await message.answer(text, reply_markup=markup)
    await UserWaiting.INPUT_COUNT_OF_CURRENCY.set()


@dp.message_handler(state=UserWaiting.INPUT_AGREEMENT)
async def send_menu_if_not_agreement(message: types.Message, state: FSMContext):
    await canceling_transaction(message, state)


@dp.message_handler(state=UserWaiting.INPUT_COUNT_OF_CURRENCY)
async def get_currency_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency_name = data['currency_name']
    if not message.text.replace('.', '', 1).isdigit():
        text = messages.OFFER_TEMPLATE.format(currency_name=currency_name)
        return await send_error_message(message, text)
    count_of_money = float(message.text)
    now_course = coin_api.get_coin_price(currency_name)
    if 0.001 < count_of_money < 2:
        count_of_currency = count_of_money
        count_of_rub = now_course * count_of_currency
    elif count_of_money >= 300:
        count_of_rub = count_of_money
        count_of_currency = count_of_rub / now_course
    else:
        text = messages.OFFER_TEMPLATE.format(currency_name=currency_name)
        return await send_error_message(message, text)
    commission_procent = 0.08  # TODO ME
    curency_commision = 40 if currency_name == 'BTC' else 20
    count_of_rub += max(100, ceil(count_of_rub * commission_procent)) + curency_commision
    count_of_currency = round(count_of_currency, 8)
    random_salt = uuid.uuid4()
    await state.update_data(
        count_of_currency=count_of_currency,
        count_of_rub=count_of_rub,
        random_salt=random_salt
    )
    data = await state.get_data()
    text = messages.ITOG_TEMPLATE.format(**data)
    inline_markup = button_to_rules.get_markup()
    await message.answer(text, reply_markup=inline_markup)
    text = f'ВВЕДИТЕ адрес {currency_name}-кошелька'
    await message.answer(text)
    await UserWaiting.INPUT_WALLET_ADRESS.set()
    await asyncio.sleep(2 * 60)  # ждём 25 минут # TODO ME
    data = await state.get_data()
    if 'random_salt' in data and data['random_salt'] == random_salt:
        text = messages.HAS_NOT_PAID_IN_TIME.format(*data)
        await message.answer(text, reply_markup=menu_key.get_markup())
        await state.finish()


@dp.message_handler(state=UserWaiting.INPUT_WALLET_ADRESS)
async def check_wallet_adress(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency_name = data['currency_name']
    wallet_adress = message.text
    if currency_name == 'LTC' and not (wallet_adress[0] in 'ML3l' and len(wallet_adress) > 32):
        text = f'ВВЕДИТЕ адрес {currency_name}-кошелька'
        return await send_error_message(message, text)
    if currency_name == 'BTC' and len(wallet_adress) > 34:
        text = f'ВВЕДИТЕ адрес {currency_name}-кошелька'
        return await send_error_message(message, text)
    await state.update_data(wallet_adress=wallet_adress)
    data = await state.get_data()
    text = messages.TO_PAY_COUNT_MESSAGE.format(**data)
    await message.answer(text)
    await message.answer(config.CARD_NUMBER)
    text = messages.TO_PAYMENT_INFO_MESSAGE.format(**data)
    await message.answer(text, reply_markup=payed_or_not_key.get_markup())
    create_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    random_salt = uuid.uuid4()
    await state.update_data(
        create_time=create_time,
        is_paid=False,
        random_salt=random_salt)

    await UserWaiting.INPUT_IS_PAID.set()
    await asyncio.sleep(2 * 60)  # TODO ME
    data = await state.get_data()
    if 'random_salt' in data and data['random_salt'] == random_salt:
        text = messages.HAS_NOT_PAID_IN_TIME.format(*data)
        await message.answer(text, reply_markup=menu_key.get_markup())
        await state.finish()


@dp.message_handler(
    Text(startswith='Я оплатил'),
    state=UserWaiting.INPUT_IS_PAID)
async def check_transaction(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['username'] = message.from_user.username
    data['user_id'] = message.from_user.id
    text = messages.FOR_OPERATOR_ORDER_TEMPLATE.format(**data)
    await dp.bot.send_message(config.OPERATOR_ID, text)

    await state.finish()

    text = messages.REQUEST_IN_PROCESSING.format(*data)
    await message.answer(text, reply_markup=menu_key.get_markup())


@dp.message_handler(
    Text(startswith='Отмена'),
    state=UserWaiting.INPUT_IS_PAID
)
async def canceling_transaction(message: types.Message, state: FSMContext):
    await state.finish()
    markup = menu_key.get_markup()
    await message.answer(messages.MENU_MESSAGE, reply_markup=markup)


@dp.message_handler(state=UserWaiting.INPUT_IS_PAID)
async def send_question(message: types.Message, state: FSMContext):
    await message.answer(messages.INFO_ABOUT_ACTIONS_IN_PAYMENT)
