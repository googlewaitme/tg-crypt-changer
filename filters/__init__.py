from aiogram import Dispatcher

from loader import dp
from .is_operator import OperatorFilter


if __name__ == "filters":
    dp.filters_factory.bind(OperatorFilter)
