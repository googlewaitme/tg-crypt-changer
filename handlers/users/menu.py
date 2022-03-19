from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from loader import dp
from data import messages, config
from keyboards.default import menu_key


@dp.message_handler(Text(["/menu", 'меню'], ignore_case=True), state='*')
async def send_menu(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    keyboard = menu_key.get_markup()
    text = messages.MENU_MESSAGE.format(
        big_procent=config.states['procent'] - 2,
        low_procent=config.states['procent'] - 4,
    )
    await message.answer(text, reply_markup=keyboard)
