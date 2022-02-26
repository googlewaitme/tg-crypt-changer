from loader import dp

from aiogram import types
from aiogram.dispatcher.filters import Text

from handlers.operators.reserve import send_reserve as send_reserve_operator


@dp.message_handler(Text('Резерв'), is_manager=True)
async def send_reserve(message: types.Message):
    await send_reserve_operator(message)
