from loader import dp, currencyes

from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text('Резерв'), is_operator=True)
async def send_reserve(message: types.Message):
    text = 'Остатки:'
    for currency in currencyes:
        text += "\n" + currency.get_resource()
    await message.answer(text)
