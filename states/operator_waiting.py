from aiogram.dispatcher.filters.state import StatesGroup, State


class ManualTransaction(StatesGroup):
    INPUT_COUNT_OF_CURRENCY = State()
    INPUT_WALLET_ADRESS = State()
    INPUT_TRANSACTION_PROCENT = State()
    CONFIRMATION = State()


class OperatorWaiting(StatesGroup):
    INPUT_TRANSACTIONS_CURRENCY = State()
    INPUT_USER_ID_FOR_BAN = State()
    INPUT_BAN_STATUS_CONFIRMATION = State()
    INPUT_TYPE_OF_TRANSACTION = State()
    INPUT_CREDIT_CARD = State()
    CALCULATE_INPUT_COUNT = State()
    CALCULATE_CHOOSE_CURRENCY = State()
