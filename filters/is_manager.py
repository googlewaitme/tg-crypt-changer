from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data.config import MANAGER_ID


class ManagerFilter(BoundFilter):
    key = 'is_manager'

    def __init__(self, is_manager: bool):
        self.is_manager = is_manager

    async def check(self, message: types.Message):
        return self.is_manager is (message.from_user.id == MANAGER_ID)
