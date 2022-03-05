from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from datetime import datetime
import asyncio
import uuid

from utils.db_api.transaction_api import TransactionApi
from utils.db_api.user_api import UserApi
from data import messages, config
from loader import dp, get_currency
from states.user_waiting import UserWaiting
from keyboards.default import (agreement_key, back_to_menu_key,
                               payed_or_not_key, menu_key)
from keyboards.inline import button_to_rules, button_to_support
from keyboards.operator.inline import confirmation_to_send


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
async def send_menu_if_not_agreement(message: types.Message, state):
    await canceling_transaction(message, state)


@dp.message_handler(
    state=UserWaiting.INPUT_COUNT_OF_CURRENCY,
    text_is_float=False)
async def send_text_must_be_float(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency_name = data['currency_name']
    text = messages.OFFER_TEMPLATE.format(currency_name=currency_name)
    return await send_error_message(message, text)


@dp.message_handler(
    state=UserWaiting.INPUT_COUNT_OF_CURRENCY,
    text_is_float=True)
async def get_currency_wallet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency_name = data['currency_name']
    currency = get_currency[currency_name]
    count_of_money = float(message.text)
    currency_amount, native_amount = currency.get_amounts(count_of_money)
    comission_amount = currency.get_commision(native_amount)
    need_to_pay = native_amount + comission_amount
    random_salt = uuid.uuid4()
    await state.update_data(
        currency_count=currency_amount,
        rub_count=need_to_pay,
        comission_count=comission_amount,
        random_salt=random_salt
    )
    data = await state.get_data()
    text = messages.ITOG_TEMPLATE.format(**data)
    inline_markup = button_to_rules.get_markup()
    await message.answer(text, reply_markup=inline_markup)
    text = f'ВВЕДИТЕ адрес {currency_name}-кошелька'
    await message.answer(text)
    await UserWaiting.INPUT_WALLET_ADRESS.set()
    await check_in_time(message, state, 2 * 60, random_salt)


@dp.message_handler(state=UserWaiting.INPUT_WALLET_ADRESS)
async def check_wallet_adress(message: types.Message, state: FSMContext):
    data = await state.get_data()
    currency_name = data['currency_name']
    currency = get_currency[currency_name]
    wallet_adress = message.text
    if not currency.check_wallet_adress(wallet_adress):
        text = f'ВВЕДИТЕ адрес {currency_name}-кошелька'
        return await send_error_message(message, text)
    data['wallet_adress'] = wallet_adress
    text = messages.TO_PAY_COUNT_MESSAGE.format(**data)
    await message.answer(text)
    await message.answer(config.CARD_NUMBER)
    text = messages.TO_PAYMENT_INFO_MESSAGE.format(**data)
    await message.answer(text, reply_markup=payed_or_not_key.get_markup())
    create_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    random_salt = uuid.uuid4()
    await state.update_data(
        wallet_adress=wallet_adress,
        create_time=create_time,
        is_paid=False,
        random_salt=random_salt
    )
    await UserWaiting.INPUT_IS_PAID.set()
    await check_in_time(message, state, 2 * 60, random_salt)


async def check_in_time(message, state, count_of_sec, random_salt):
    await asyncio.sleep(count_of_sec)
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
    user = UserApi(message.from_user.id).get()
    transaction = TransactionApi().create(
        user=user,
        **data
    )
    data['username'] = message.from_user.username
    data['user_id'] = message.from_user.id
    text = messages.FOR_OPERATOR_ORDER_TEMPLATE.format(**data)
    markup = confirmation_to_send.get_markup(transaction.id)
    await dp.bot.send_message(config.OPERATOR_ID, text, reply_markup=markup)

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
