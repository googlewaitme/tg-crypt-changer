from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from data import messages


@dp.message_handler(Text(startswith='Купим вашу крипту'))
async def send_info_about_selling_currency(message: types.Message):
    await message.answer(messages.INFO_ABOUT_SELLING_CURRENCY)

