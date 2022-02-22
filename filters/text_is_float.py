from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class TextIsFloat(BoundFilter):
    key = 'text_is_float'

    def __init__(self, text_is_float: bool):
        self.text_is_float = text_is_float

    async def check(self, message: types.Message):
        return message.text.replace('.', '', 1).isdigit() is self.text_is_float
