from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from keyboards.default import operator_menu_key


@dp.message_handler(
    is_operator=True,
    state='*',
    content_types=types.ContentTypes.ANY)
async def bot_echo(message: types.Message, state: FSMContext):
    markup = operator_menu_key.get_markup()
    await message.answer('Меню', reply_markup=markup)
    await state.finish()
