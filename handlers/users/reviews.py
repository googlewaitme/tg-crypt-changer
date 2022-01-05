from aiogram import types
from aiogram.dispatcher.filters import Text

from data import messages
from loader import dp


@dp.message_handler(Text(startswith='Отзывы'))
async def send_info_about_reviews(message: types.Message):
    await message.answer(messages.INFO_ABOUT_REVIEWS)
