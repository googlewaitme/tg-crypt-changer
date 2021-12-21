from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from data import messages
from keyboards.default import menu_key


@dp.message_handler(Text(["/menu", 'меню'], ignore_case=True), state='*')
async def send_menu(message: types.Message):
    keyboard = menu_key.get_markup()
    text = messages.MENU_MESSAGE
    await message.answer(text, reply_markup=keyboard)
