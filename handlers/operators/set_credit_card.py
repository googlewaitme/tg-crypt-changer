from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from states.operator_waiting import OperatorWaiting
from data.config import states
from data import messages
from keyboards.default import cancel_button, operator_set_new_card_key
from keyboards.operator.default import operator_menu_key


def is_right_input_of_card_number(message: types.Message):
    text = message.text
    return text.isdigit() and len(text) == 16


@dp.message_handler(Text('💳'), is_operator=True)
async def send_now_card(message: types.Message):
    markup = operator_set_new_card_key.get_markup()
    text = "<code>" + states['card_number'] + "</code>"
    await message.answer(text, reply_markup=markup)


@dp.message_handler(Text('Загрузить карту'), is_operator=True)
async def set_credit_card(message: types.Message, state: FSMContext):
    await OperatorWaiting.INPUT_CREDIT_CARD.set()
    markup = cancel_button.get_markup()
    await message.answer('Введите номер карты:', reply_markup=markup)


@dp.message_handler(
    Text(messages.CANCEL_BUTTON_TEXT),
    state=OperatorWaiting.INPUT_CREDIT_CARD,
    is_operator=True
)
async def return_menu(message: types.Message, state: FSMContext):
    menu = operator_menu_key.get_markup()
    await message.answer(messages.MENU_MESSAGE, reply_markup=menu)
    await state.finish()


@dp.message_handler(
    is_right_input_of_card_number,
    state=OperatorWaiting.INPUT_CREDIT_CARD,
    is_operator=True
)
async def set_card(message: types.Message, state: FSMContext):
    menu = operator_menu_key.get_markup()
    states['card_number'] = message.text
    await message.answer(messages.OPERATOR_CARD_SETTED, reply_markup=menu)
    await state.finish()


@dp.message_handler(
    state=OperatorWaiting.INPUT_CREDIT_CARD,
    is_operator=True
)
async def send_error_card_number(message: types.Message, state: FSMContext):
    await message.answer(messages.INPUTING_ERROR_MESSAGE)
