from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db_api.user_api import UserApi


class RegisterUser(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        user = UserApi(telegram_id=message.from_user.id)
        if not user.is_exist():
            user.create()
        else:
            user.set_last_visited()
