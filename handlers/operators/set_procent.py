from loader import dp

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.operator_waiting import OperatorWaiting
from data.config import states
from keyboards.default import back_to_menu_key
from keyboards.operator.default import operator_menu_key


@dp.message_handler(Text('Процент📌'))
async def send_question(message: types.Message):
    now_procent = states['procent']
    text = f"Текущий процент: {now_procent}"
    text += "\nВведите новый процент:"
    markup = back_to_menu_key.get_markup()
    await message.answer(text, reply_markup=markup)
    await OperatorWaiting.INPUT_NEW_PROCENT.set()


@dp.message_handler(
    text_is_int=False,
    state=OperatorWaiting.INPUT_NEW_PROCENT
)
async def send_error_message(message: types.Message):
    await message.answer('Процент должен быть целым числом')


@dp.message_handler(
    text_is_int=True,
    state=OperatorWaiting.INPUT_NEW_PROCENT)
async def set_new_procent(message: types.Message, state: FSMContext):
    procent = int(message.text)
    states['procent'] = procent
    text = f"Текущий процент: {procent}"
    menu_key = operator_menu_key.get_markup()
    await message.answer(text, reply_markup=menu_key)
    await state.finish()
