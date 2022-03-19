from aiogram import types

from loader import dp
from keyboards.default import menu_key
from data import messages, config


@dp.message_handler(state='*', content_types=types.ContentTypes.ANY)
async def bot_echo(message: types.Message):
    markup = menu_key.get_markup()
    text = messages.MENU_MESSAGE.format(
        big_procent=config.states['procent'] - 2,
        low_procent=config.states['procent'] - 4
    )
    await message.answer(text, reply_markup=markup)
