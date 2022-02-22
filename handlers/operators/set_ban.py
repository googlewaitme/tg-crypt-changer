from loader import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram import types

from utils.db_api.models import User
from keyboards.default import (confirmation_key, operator_menu_key,
                               back_to_menu_key)
from data import messages
from states.operator_waiting import OperatorWaiting


@dp.message_handler(Text('Бан'), is_operator=True)
async def begin_set_ban(message: types.Message, state: FSMContext):
    markup = back_to_menu_key.get_markup()
    await OperatorWaiting.INPUT_USER_ID_FOR_BAN.set()
    await message.answer(messages.INPUT_USER_ID_FOR_BAN, reply_markup=markup)


@dp.message_handler(
    text_is_int=False,
    state=OperatorWaiting.INPUT_USER_ID_FOR_BAN)
async def send_information_about_error(message: types.Message):
    await message.answer(messages.INPUTING_ERROR_MESSAGE)


@dp.message_handler(
    text_is_int=True,
    state=OperatorWaiting.INPUT_USER_ID_FOR_BAN)
async def set_ban(message: types.Message, state: FSMContext):
    user_id = int(message.text)
    model = User.get_or_none(User.telegram_id == user_id)
    if model:
        text = f"Пользователь {user_id}"
        text += ("🔴 Заблокирован" if model.is_baned else "🟢 Активен")
        text += "\nИзменить статус пользователя?"
        markup = confirmation_key.get_markup()
        await OperatorWaiting.INPUT_BAN_STATUS_CONFIRMATION.set()
        await message.answer(text, reply_markup=markup)
        await state.update_data(user_id=user_id)
    else:
        await message.answer('Пользователь не найден')


@dp.message_handler(
    Text(messages.CONFIRMATION_BUTTON_TEXT),
    state=OperatorWaiting.INPUT_BAN_STATUS_CONFIRMATION)
async def change_ban_status(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    model = User.get_or_none(User.telegram_id == user_id)
    model.is_baned = not model.is_baned
    model.save()
    text = f"Пользователь {user_id}" + ("🔴" if model.is_baned else "🟢")
    menu_key = operator_menu_key.get_markup()
    await message.answer(text, reply_markup=menu_key)
    await state.finish()
