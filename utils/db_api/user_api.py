from .models import User
from datetime import datetime


class UserApi():
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id

    def is_exist(self):
        query = User.select().where(User.telegram_id == self.telegram_id)
        return query.exists()

    def get(self):
        return User.get(telegram_id=self.telegram_id)

    def create(self):
        User.create(
            telegram_id=self.telegram_id,
            is_baned=False,
            join_date=datetime.now()
        )

    def is_baned(self):
        user = User.get(User.telegram_id == self.telegram_id)
        return user.is_baned
