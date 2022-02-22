from loader import dp, coin_api

from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text('Резерв'))
async def send_reserve(message: types.Message):
    await message.answer(coin_api.get_resurces())
