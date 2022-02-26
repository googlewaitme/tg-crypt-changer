from loader import dp

from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text('Промокоды'), is_manager=True)
async def will_be_soon(message: types.Message):
    """
    Промокоды
    """
    await message.answer('Промокоды в разработке')
