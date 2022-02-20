from aiogram.dispatcher.filters.state import StatesGroup, State


class OperatorWaiting(StatesGroup):
    INPUT_CREDIT_CARD = State()
    CALCULATE_INPUT_COUNT = State()
    CALCULATE_CHOOSE_CURRENCY = State()
