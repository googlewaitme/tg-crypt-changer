from aiogram.dispatcher.filters.state import StatesGroup, State



class UserWaiting(StatesGroup):
    CALCULATE_CHOOSE_CURRENCY = State()
    CALCULATE_INPUT_COUNT = State()
    INPUT_AGREEMENT = State()
    INPUT_COUNT_OF_CURRENCY = State()
    INPUT_WALLET_ADRESS = State()
    INPUT_IS_PAID = State()
