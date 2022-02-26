from loader import dp

from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.inline import currencyes_tumbler_markup
from keyboards.inline.currencyes_tumbler_markup import tumbler_cb
from data.config import states, CURRENCYES


@dp.message_handler(Text('🕹️'), is_operator=True)
async def send_currencyes(message: types.Message):
    await message.answer(
        "Нажатием включите или отключите криптовалюты",
        reply_markup=currencyes_tumbler_markup.get_markup())


@dp.callback_query_handler(tumbler_cb.filter(currency_name='all'))
async def all_tumbler_status(query: types.CallbackQuery, callback_data: dict):
    if callback_data['in_work'] == 'True':
        states['currency_in_work'] = CURRENCYES.copy()
    else:
        states['currency_in_work'] = []
    await update_tumbler_message(query)
    await query.answer()


@dp.callback_query_handler(tumbler_cb.filter(in_work='True'))
async def delete_from_in_work(query: types.CallbackQuery, callback_data: dict):
    currency_name = callback_data['currency_name']
    if currency_name in states['currency_in_work']:
        copy_currencyes = states['currency_in_work']
        copy_currencyes.remove(currency_name)
        states['currency_in_work'] = copy_currencyes
    await update_tumbler_message(query)
    await query.answer()


@dp.callback_query_handler(tumbler_cb.filter(in_work='False'))
async def add_from_in_work(query: types.CallbackQuery, callback_data: dict):
    currency_name = callback_data['currency_name']
    if currency_name not in states['currency_in_work']:
        copy_currencyes = states['currency_in_work']
        copy_currencyes.append(currency_name)
        states['currency_in_work'] = copy_currencyes
    await update_tumbler_message(query)
    await query.answer()


async def update_tumbler_message(query):
    markup = currencyes_tumbler_markup.get_markup()
    await query.message.edit_reply_markup(markup)
