from loader import dp

from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text('Конкурс'), is_manager=True)
async def will_be_soon(message: types.Message):
    """
    Конкурсы
    """
    await message.answer('Конкурсы в разработке')
