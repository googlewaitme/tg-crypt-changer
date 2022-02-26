from loader import dp

from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text('Статистика'), is_manager=True)
async def will_be_soon(message: types.Message):
    """
    Отображение кол-во пользователей за день/месяц/все время.
    Статистика по новым пользователям за день/месяц/все время.
    Отображение статистики по отдельным пригласительным кодам.
    """
    await message.answer('Статистика в разработке')
