from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data.config import OPERATOR_ID


class OperatorFilter(BoundFilter):
    key = 'is_operator'

    def __init__(self, is_operator):
        self.is_operator = is_operator

    async def check(self, message: types.Message):
        return self.is_operator is (message.from_user.id == OPERATOR_ID)
