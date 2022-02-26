from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.manager.default import menu_key


@dp.message_handler(is_manager=True, state='*')
async def send_echo(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    await message.answer('Меню', reply_markup=menu_key.get_markup())
