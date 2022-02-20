from aiogram.dispatcher.filters.state import StatesGroup, State


class OperatorWaiting(StatesGroup):
    INPUT_CREDIT_CARD = State()
