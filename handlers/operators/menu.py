from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from keyboards.operator.default import operator_menu_key


@dp.message_handler(Text('Меню'), is_operator=True, state='*')
async def send_menu(message: types.Message, state: FSMContext):
    markup = operator_menu_key.get_markup()
    await message.answer('Меню', reply_markup=markup)
    await state.finish()
