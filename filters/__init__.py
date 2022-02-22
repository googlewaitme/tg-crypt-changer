from aiogram import Dispatcher

from loader import dp
from .is_operator import OperatorFilter
from .text_is_float import TextIsFloat
from .text_is_integer import TextIsInt


if __name__ == "filters":
    dp.filters_factory.bind(OperatorFilter)
    dp.filters_factory.bind(TextIsFloat)
    dp.filters_factory.bind(TextIsInt)
