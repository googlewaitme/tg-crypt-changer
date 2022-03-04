from utils.db_api.models import Cashbox, Transaction
import datetime


class CashboxApi:
    def __init__(self):
        self.set_cashbox()

    def set_cashbox(self):
        model, created = Cashbox.get_or_create(closed=None)
        self.model = model

    def get_cashbox(self):
        return self.model

    def get_list_transactions(self):
        text = 'Транзакции за смену:'
        query = Transaction.select().where(
            (Transaction.cashbox == self.model)
            & (Transaction.is_operator_checked == True)
        )
        for transaction in query:
            text += "\n\n💵💵💵💵💵\n" + str(transaction)
            self.model.passed_operations += 1
            self.model.total_sum += transaction.comission_count
        self.model.save()
        return text

    def get_params(self):
        opened_time = self.model.opened.strftime("%d/%m/%Y, %H:%M:%S")
        if self.model.closed is None:
            closed_time = 'Смена в работе🚀'
        else:
            closed_time = self.model.closed.strftime("%d/%m/%Y, %H:%M:%S")

        text = f"Смена номер: {self.model.id}"
        text += "\nНачало смены: " + opened_time
        text += '\nКонец смены: ' + closed_time
        text += f"\nСумма: {self.model.total_sum}"
        text += f"\nКол-во операций: {self.model.passed_operations}"
        return text

    def close_cashbox(self):
        self.model.closed = datetime.datetime.now()
        self.model.save()

    def create_new_cashbox(self):
        if self.model.closed is None:
            self.close_cashbox()
        self.set_cashbox()
