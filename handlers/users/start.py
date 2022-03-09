from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from utils.db_api.user_api import UserApi
from loader import dp
from keyboards.default import menu_key


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = f"Привет, {message.from_user.full_name}!"
    markup = menu_key.get_markup()
    await message.answer(text, reply_markup=markup)
    await set_referal_token(message)


async def set_referal_token(message):
    args = message.text.split()
    if len(args) == 2:
        user = UserApi(message.from_user.id)
        token = user.get_referal_token()
        if token is None:
            user.set_referal_token(args[1])
