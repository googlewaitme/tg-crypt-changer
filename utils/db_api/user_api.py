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
            join_date=datetime.now(),
            last_visit_date=datetime.now()
        )

    def is_baned(self):
        user = User.get(User.telegram_id == self.telegram_id)
        return user.is_baned

    def set_last_visited(self):
        query = User.update(last_visit_date=datetime.now())
        query = query.where(User.telegram_id == self.telegram_id)
        query.execute()

    def get_referal_token(self):
        user = self.get()
        return user.referal_token

    def set_referal_token(self, referal_token):
        user = self.get()
        user.referal_token = referal_token
        user.save()
