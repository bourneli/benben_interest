# -*- coding: utf-8 -*-
#
# 账号对象，用于集体管理存款，计算利息
#


from datetime import timedelta
import toolkit
from deposit import Deposit


class Account:
    def __init__(self, rate_history=[]):
        self._all_deposit = {}
        self._rate_history = rate_history

    def __str__(self):
        sorted_date = self._all_deposit.keys()
        sorted_date.sort()
        return "\n".join([str(self._all_deposit[date]) for date in sorted_date])

    def total_amount(self):
        return sum([deposit.amount() for deposit in self._all_deposit.values()])

    def save(self, deposit):
        if deposit.start_date() in self._all_deposit:
            self._all_deposit[deposit.start_date()].save(deposit.amount())
        else:
            self._all_deposit[deposit.start_date()] = deposit

    def withdraw(self, date, amount):

        # print "amount %s" % amount
        earn = 0
        # TODO:优化，添加数据检查
        date_list = sorted(self._all_deposit.keys(), reverse=True)
        while date_list:
            recent_date = date_list.pop(0)
            if recent_date >= date:
                continue

            earn += self._all_deposit[recent_date].interest(date, amount, self._rate_history)  # 计算利息
            withdraw_amount = self._all_deposit[recent_date].withdraw(amount)  # 取钱

            # print "withdraw amount %s" % withdraw_amount
            amount -= withdraw_amount
            # print "amount %s" % amount
            if 0 == amount:
                break

        return earn

    #
    # 计算所有deposit中最早的一个
    #
    def _earliest_date(self):
        return min(self._all_deposit.keys())

    #
    # 处理一年前的deposit账号，计算利息，并将money存放在明天的账号中
    #
    def cycle(self, storage_date):

        if not self._all_deposit:
            return 0.0  # 空,直接返回

        one_year_ago = toolkit.add_months_obj(storage_date, -12)
        if one_year_ago < self._earliest_date():
            return 0.0  # 没有满一年，直接返回

        # 满一年，
        # 1 计算利息
        # 2 取完账户的所有存款
        # 3 存到明天的账户
        earn = 0.0
        if one_year_ago in self._all_deposit:
            earn = self._all_deposit[one_year_ago].interest_all(storage_date, self._rate_history)
            all_inside = self._all_deposit[one_year_ago].withdraw_all()
            tomorrow_deposit = Deposit(storage_date + timedelta(days=1), all_inside)
            self.save(tomorrow_deposit)

        return earn

    #
    # 计算利息
    #
    def interest(self, flows):
        earn = 0.0
        for storage_date, storage_amount in flows:
            total_amount = self.total_amount()

            # 计算当前的存量
            if storage_amount > total_amount:
                self.save(Deposit(storage_date, storage_amount - total_amount))
            elif storage_amount < total_amount:
                earn += self.withdraw(storage_date, total_amount - storage_amount)

            # 取出一年前的数据，计算利息，并且存到明天的账号中
            earn += self.cycle(storage_date)

        return earn
