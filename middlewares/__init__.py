from loader import dp

from .register_user import RegisterUser
from .user_is_baned import UserIsBaned
from aiogram.contrib.middlewares.logging import LoggingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(RegisterUser())
    dp.middleware.setup(UserIsBaned())
    dp.middleware.setup(LoggingMiddleware())
