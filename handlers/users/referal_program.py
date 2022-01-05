from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp


@dp.message_handler(Text(startswith='Партнёрка'))
async def send_referal_url(message: types.Message):
    user_id = message.from_user.id
    url = f'https://telegram.me/Flash_Crypt_ExchangeBot?start={user_id}'
    await message.answer(url)
