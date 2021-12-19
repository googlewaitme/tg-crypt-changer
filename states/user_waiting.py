from aiogram.dispatcher.filters.state import StatesGroup, State


class UserWaiting(StatesGroup):
    CALCULATE_CHOOSE_CURRENCY = State()
    CALCULATE_INPUT_COUNT = State()
