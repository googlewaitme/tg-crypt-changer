from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class TextIsPositiveInt(BoundFilter):
    key = 'text_is_positive_int'

    def __init__(self, text_is_positive_int: bool):
        self.text_is_positive_int = text_is_positive_int

    async def check(self, message: types.Message):
        return self.is_positive_int(message.text) is self.text_is_positive_int

    def is_positive_int(self, text):
        if not text.isdigit():
            return False
        return int(text) >= 0
