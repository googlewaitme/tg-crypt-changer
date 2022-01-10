from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

from utils.db_api.user_api import UserApi
from data import messages


class UserIsBaned(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        user = UserApi(telegram_id=message.from_user.id)
        if user.is_exist() and user.is_baned():
            await message.answer(messages.BANNED_MESSAGE)
            raise CancelHandler()

