from aiogram import types

from loader import dp
from keyboards.default import menu_key
from data import messages


@dp.message_handler(state='*', content_types=types.ContentTypes.ANY)
async def bot_echo(message: types.Message):
    markup = menu_key.get_markup()
    await message.answer(messages.MENU_MESSAGE, reply_markup=markup)

