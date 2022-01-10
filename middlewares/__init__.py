from aiogram import Dispatcher

from loader import dp
from .register_user import RegisterUser
from .user_is_baned import UserIsBaned


if __name__ == "middlewares":
    dp.middleware.setup(RegisterUser())
    dp.middleware.setup(UserIsBaned())

