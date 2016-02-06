# -*- coding: utf-8 -*-
#
# 每笔存款对象
#
import toolkit
from datetime import datetime

Y = 360.0  # 一年的近似天数


class Deposit:
    def __init__(self, start_date, amount):
        self._start_date = start_date
        self._amount = amount

    def __str__(self):
        return "%s,%d" % (self._start_date.strftime("%Y/%m/%d"), self._amount)

    def start_date(self):
        return self._start_date

    def amount(self, amount=None):
        if amount is None:
            return self._amount
        else:
            self.save(amount)

    #
    # 取钱，如果取出的金额大于已有的金额，也只能取出已有的金额，并且当前金额会为0
    # @param withdraw_amount 取出的金额
    # @return 取出的金额
    #
    def withdraw(self, withdraw_amount):

        assert withdraw_amount >= 0, "required amount %d is less than 0" % withdraw_amount
        diff_amount = 0

        if withdraw_amount < self._amount:
            diff_amount = withdraw_amount
            self._amount -= withdraw_amount
        else:
            diff_amount = self._amount
            self._amount = 0

        return diff_amount

    #
    # 取出所有的钱
    #
    def withdraw_all(self):
        return self.withdraw(self._amount)

    #
    # 存钱
    #
    def save(self, amount):
        assert amount >= 0, "amount %d is less than 0" % amount
        self._amount += amount

    #
    # 计算利息，核心逻辑
    # @param statis_date 计算日期
    # @param withdraw_amount 本金
    # @param r 利率表，提供不同时间段的利率
    # TODO: 根据不同时段的利率表计算利息
    #
    def interest(self, statis_date, withdraw_amount, rate_history):

        diff_amount = withdraw_amount if withdraw_amount <= self._amount else self._amount
        assert diff_amount >= 0, "diff_amount = %d is less than 0" % diff_amount

        # 不同月份的自然月天数
        days_3m = (toolkit.add_months_obj(self._start_date, 3) - self._start_date).days
        days_6m = (toolkit.add_months_obj(self._start_date, 6) - self._start_date).days
        days_9m = (toolkit.add_months_obj(self._start_date, 9) - self._start_date).days
        days_12m = (toolkit.add_months_obj(self._start_date, 12) - self._start_date).days

        n = (statis_date - self._start_date).days
        assert 0 <= n <= days_12m, "n=%d is out of one year" % n

        # 详细的分段计算公式，参考文档:<home>/doc/利息计算公式.docx
        earn_interest = diff_amount
        r = rate_history.get_rates(self._start_date)
        if 0 <= n < 7:
            earn_interest *= r['day_1'] * n / Y
        elif 7 <= n < days_3m:
            earn_interest *= r['day_7'] * n / Y
        elif days_3m <= n < days_3m + 7:
            earn_interest *= 0.25 * r['month_3'] + r['day_1'] * (n - days_3m) / Y
        elif days_3m + 7 <= n < days_6m:
            earn_interest *= 0.25 * r['month_3'] + r['day_7'] * (n - days_3m) / Y
        elif days_6m <= n < days_6m + 7:
            earn_interest *= 0.5 * r['month_6'] + r['day_1'] * (n - days_6m) / Y
        elif days_6m + 7 <= n < days_9m:
            earn_interest *= 0.5 * r['month_6'] + r['day_7'] * (n - days_6m) / Y
        elif days_9m <= n < days_9m + 7:
            earn_interest *= 0.25 * r['month_3'] + 0.5 * r['month_6'] + r['day_1'] * (n - days_9m) / Y
        elif days_9m + 7 <= n < days_12m:
            earn_interest *= 0.25 * r['month_3'] + 0.5 * r['month_6'] + r['day_7'] * (n - days_9m) / Y
        elif n == days_12m:
            earn_interest *= r['year_1']
        else:
            raise Exception("never thrown")

        return earn_interest

    #
    # 计算所有利息
    #
    def interest_all(self, date, rate):
        return self.interest(date, self._amount, rate)
