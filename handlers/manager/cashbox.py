from loader import dp, cashbox_api

from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text('Касса'), is_manager=True)
async def send_cashbox_information(message: types.Message):
    """
    1) Отправляет список всех операций за смену:
       {сумма транзакции} {профит}
       {дата} {криптовалюта}
    2) Отправляет кол-во обменов, сумму профита и общий оборот за день
    3) Закрывает смену и открывает новую
    """
    list_transactions = cashbox_api.get_list_transactions()
    await message.answer(list_transactions)

    cashbox_api.close_cashbox()
    params_of_cashbox = cashbox_api.get_params()
    await message.answer(params_of_cashbox)

    cashbox_api.create_new_cashbox()

    params_of_new_cashbox = cashbox_api.get_params()
    await message.answer(params_of_new_cashbox)
