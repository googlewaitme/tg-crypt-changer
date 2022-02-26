from loader import dp

from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text('История CB'), is_manager=True)
async def will_be_soon(message: types.Message):
    """
    История транзакций
    """
    await message.answer('История транзакций в разработке')
