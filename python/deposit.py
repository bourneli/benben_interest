# -*- coding: utf-8 -*-

from diff import NatureDateDiff, StrictDateDiff

# 每笔存款
class Deposit:
    def __init__(self, start_date, amount, mode="nature"):
        self.start_date = start_date
        self.amount = amount
        if 'nature' == mode:
            # print "nature"
            self.differ = NatureDateDiff()
        else:
            # print "strict"
            self.differ = StrictDateDiff()

    def __str__(self):
        return "%s,%d" % (self.start_date.strftime("%Y/%m/%d"), self.amount)

    def withdraw(self, withdraw_amount):
        diff_amount = 0

        if withdraw_amount < self.amount:
            diff_amount = withdraw_amount
            self.amount -= withdraw_amount
        else:
            diff_amount = self.amount
            self.amount = 0

        return diff_amount

    def interest(self, statis_date, withdraw_amount, rate_map={}):
        diff_amount = withdraw_amount if withdraw_amount <= self.amount else self.amount
        (diff_year_1, diff_month_6, diff_month_3, diff_day_7, diff_day_1) = self.differ.diff(self.start_date,
                                                                                             statis_date)

        return diff_amount * (
            diff_year_1 * rate_map["year_1"] +
            diff_month_6 * rate_map["month_6"] * 0.5 +
            diff_month_3 * rate_map["month_3"] * 0.25 +
            diff_day_7 * rate_map["day_7"] * (7 / 360.0) +
            diff_day_1 * rate_map["day_1"] * (1 / 360.0))

