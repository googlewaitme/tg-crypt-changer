from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from keyboards.default import menu_key


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = f"Привет, {message.from_user.full_name}!"
    markup = menu_key.get_markup()
    await message.answer(text, reply_markup=markup)
