from loader import dp
from aiogram import types
from keyboards.default import operator_menu_key


@dp.message_handler(is_operator=True)
async def send_menu(message: types.Message):
    markup = operator_menu_key.get_markup()
    await message.answer('Меню', reply_markup=markup)
