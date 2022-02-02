from peewee import *


database = SqliteDatabase('app.db')


def create_tables():
    with database:
        database.create_tables([User, Transaction])


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    telegram_id = IntegerField(unique=True)
    is_baned = BooleanField(default=False)
    join_date = DateTimeField()


class Transaction(BaseModel):
    user = ForeignKeyField(User)
    currency_name = CharField(max_length=10)
    currency_count = FloatField()
    rub_count = FloatField()
    comission_count = FloatField()
    create_date = DateTimeField()
    is_paid = BooleanField(default=False)
    is_operator_checked = BooleanField(default=False)


if __name__ == '__main__':
    create_tables()
