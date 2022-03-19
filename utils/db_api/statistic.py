from utils.db_api.models import *
from datetime import date, timedelta


class NewUsersStat:
    @staticmethod
    def get_stat_text():
        today = date.today()
        one_day_ago = today - timedelta(days=1)
        month_ago = today - timedelta(days=30)
        stat_one_day = NewUsersStat.get_stat_by_dates(one_day_ago, today)
        stat_month = NewUsersStat.get_stat_by_dates(month_ago, today)
        all_new_users = NewUsersStat.get_all_count()
        return f"""Новые пользователи
        За один день:{stat_one_day}
        За последние 30 дней: {stat_month}
        Всего: {all_new_users}\n"""

    @staticmethod
    def get_stat_by_dates(start_day, end_day):
        stat = User.select().where(
            (User.join_date >= start_day) & (User.join_date <= end_day)
        ).count()
        return stat

    @staticmethod
    def get_all_count():
        return User.select().count()


class UsersStat:
    @staticmethod
    def get_stat_text():
        today = date.today()
        tomorrow = today + timedelta(days=1)
        month_ago = today - timedelta(days=30)
        stat_one_day = UsersStat.get_stat_by_dates(today, tomorrow)
        stat_month = UsersStat.get_stat_by_dates(month_ago, today)
        all_new_users = UsersStat.get_all_count()
        return f"""Авторизации пользователей
        За один день:{stat_one_day}
        За последние 30 дней: {stat_month}
        Всего: {all_new_users}\n"""

    @staticmethod
    def get_stat_by_dates(start_day, end_day):
        stat = User.select().where(
            (User.last_visit_date >= start_day)
            & (User.last_visit_date <= end_day)
        ).count()
        return stat

    @staticmethod
    def get_all_count():
        return User.select().count()


class ReferalStat:
    @staticmethod
    def get_stat_text():
        query = User.select(User.referal_token).distinct()
        text = 'Реферальные программы:\n'
        for el in query:
            if el.referal_token is None:
                continue
            count = User.select().where(
                User.referal_token == el.referal_token
            ).count()
            text += f"{el.referal_token} : {count}\n"
        return text
