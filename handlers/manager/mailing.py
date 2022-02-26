from loader import dp

from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text('Рассылка'), is_manager=True)
async def will_be_soon(message: types.Message):
    """
    Рассылка
    """
    await message.answer('Рассылка в разработке')
