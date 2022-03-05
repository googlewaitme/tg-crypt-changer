from data import config


CANCEL_BUTTON_TEXT = 'Отмена'
CONFIRMATION_BUTTON_TEXT = 'Подтверждаю'

URL_TO_OPERATOR = f'<a href="{config.URL_TO_OPERATOR}">ОПЕРАТОР</a>'

INFO_ABOUT_REVIEWS = """https://t.me/Flasher_Exchange_Book"""

FOR_OPERATOR_ORDER_TEMPLATE = """Валюта: {currency_name}
Кошелёк: <code>{wallet_adress}</code>
Количество монет: {currency_count}
Количество рублей: {rub_count}
Дата и время создания: {create_time}
Айди пользователя: {user_id}
Пользователь: @{username}"""

INFO_ABOUT_SELLING_CURRENCY = """Для продажи криптовалюты обратитесь к @Flasher_boss"""

MENU_MESSAGE = """SoNic Ex  Приветствую, я SoNic! Доставлю Ваши монеты  быстро и без потерь

Услуги обмена :
1 Обмен  8%
2 Обмен  6%
После 2-го обмена по кругу """


AGREEMENT = f"""Нажатием кнопки
Я СОГЛАШАЮСЬ , вы подтверждаете что ознакомились и согласны с правилами обмена сервиса SoNic Ex по ссылке ниже
<a href="{config.URL_TO_RULES}">Правила SONIX</a>"""


OFFER_TEMPLATE = """У Нас Самый Выгодный Курс Обмена 
Обмен проходит по курсу :
1 Обмен  8%
2 Обмен  6%
После 2-го обмена по кругу 

На какую сумму Вы хотите купить {currency_name}?
(Напишите сумму : от 0.001 {currency_name} или от 300 руб )
"""


ITOG_TEMPLATE = """Сумма к оплате составит: {rub_count} рублей 
Вы получите: {currency_count} {currency_name}

Оплата принимается на карту  банка, QIWI кошелёк любым удобным для Вас способом (с QIWI и других ЭПС, карты любого банка и терминалов)

При переводе средств на указанные Вам реквизиты, Вы подтверждаете, что полностью ознакомились с  правилами:"""


INPUTING_ERROR_MESSAGE = """НЕКОРРЕКТНЫЙ ВВОД ИЛИ НЕКОРРЕКТНОЕ ЗНАЧЕНИЕ"""

INPUT_USER_ID_FOR_BAN = """Введите id пользователя для блокировки или разблокировки"""

TO_PAY_COUNT_MESSAGE = """<b>Сумма к оплате:</b> {rub_count} руб

<b>Заявка действительна:</b> 25 минут

РЕКВИЗИТЫ"""


OPERATOR_MANUALLY_ITOG = """Подтвердите перевод:
<b>{currency_name}:</b> {currency_count}
<b>Рубли:</b> {rub_count}
<b>Адрес:</b> {wallet_adress}"""


TO_PAYMENT_INFO_MESSAGE = """После успешного перевода денег по указанным реквизитам нажмите на кнопку « Я оплатил(а)» или же Вы можете отменить данную заявку нажав на кнопку « Отменить заявку»

Покупка: {currency_count} {currency_name}
на кошелек:
<code>{wallet_adress}</code>

Если Вы перевели неправильную сумму то заявка будет считаться неоплаченной или не получили Транзакцию в течении 10 мин то Сразу сообщите об этом """ + URL_TO_OPERATOR


HAS_NOT_PAID_IN_TIME = """От тебя не дождались реакции в течении 25 минут, заявка аннулирована.
По всем вопросам обращаться к """ + URL_TO_OPERATOR


REQUEST_IN_PROCESSING = """ВАША ЗАЯВКА В ОБРАБОТКЕ

ОЖИДАЙТЕ ПОСТУПЛЕНИЕ СРЕДСТВ 
на случай помощи, пишите """ + URL_TO_OPERATOR


INFO_ABOUT_ACTIONS_IN_PAYMENT = """Нажмите кнопку <b>Отмена</b> или <b>Я оплатил</b>"""


TRANSACTION_IS_PASSED = """Транзакция подтверждена. Ожидайте поступление средств"""

TRANSACTION_IS_CANCELED = """Транзакция отклонена."""


BANNED_MESSAGE = """Вы заблокированы. Разблокировка у """ + URL_TO_OPERATOR


CURRENCY_NOT_IN_WORK = """
Простите, данная криптовалюты сейчас не доступна для покупки.
Попробуйте позже или обратитесь к поддержке."""

OPERATOR_CARD_SETTED = """Карта установлена"""
