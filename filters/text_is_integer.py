from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class TextIsInt(BoundFilter):
    key = 'text_is_float'

    def __init__(self, text_is_int: bool):
        self.text_is_int = text_is_int

    async def check(self, message: types.Message):
        return message.text.isdigit() is self.text_is_int
