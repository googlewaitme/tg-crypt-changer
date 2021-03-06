from aiogram import Dispatcher

from loader import dp
from .is_operator import OperatorFilter
from .is_manager import ManagerFilter
from .text_is_float import TextIsFloat
from .text_is_integer import TextIsInt
from .text_is_positive_int import TextIsPositiveInt


if __name__ == "filters":
    dp.filters_factory.bind(OperatorFilter)
    dp.filters_factory.bind(ManagerFilter)
    dp.filters_factory.bind(TextIsFloat)
    dp.filters_factory.bind(TextIsInt)
    dp.filters_factory.bind(TextIsPositiveInt)
