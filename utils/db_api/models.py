from peewee import *
import datetime


database = SqliteDatabase('app.db')


def create_tables():
    with database:
        database.create_tables([User, Transaction, Cashbox])


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    telegram_id = IntegerField(unique=True)
    is_baned = BooleanField(default=False)
    join_date = DateTimeField()
    last_visit_date = DateTimeField()
    referal_token = CharField(max_length=100, null=True)


class Cashbox(BaseModel):
    opened = DateTimeField(default=datetime.datetime.now)
    closed = DateTimeField(null=True)
    passed_operations = IntegerField(default=0)
    total_sum = IntegerField(default=0)


class Transaction(BaseModel):
    user = ForeignKeyField(User, backref='transactions')
    cashbox = ForeignKeyField(Cashbox, null=True, backref='transactions')
    currency_name = CharField(max_length=10)
    currency_count = FloatField()
    rub_count = FloatField()
    comission_count = FloatField()
    create_date = DateTimeField(default=datetime.datetime.now)
    is_paid = BooleanField(default=False)
    is_operator_checked = BooleanField(default=False)
    wallet_adress = CharField(max_length=200, null=True)
    status = CharField(max_length=200, default='pending')

    def __str__(self):
        create_date = self.create_date.strftime("%d/%m/%Y, %H:%M:%S")
        info = f"{self.currency_name} {self.wallet_adress}"
        info += f"\n{create_date}"
        info += f"\nКомиссия: {self.comission_count}"
        info += f"\nСумма: {self.rub_count}"
        return info


if __name__ == '__main__':
    create_tables()
