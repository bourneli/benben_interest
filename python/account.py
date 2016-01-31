# -*- coding: utf-8 -*-

class Account:


    def __init__(self, bank_rate={}):
        self.flow = {}
        self.bank_rate = bank_rate

    def __str__(self):
        sorted_date = self.flow.keys()
        sorted_date.sort()
        return "\n".join([str(self.flow[date]) for date in sorted_date])

    def total_amount(self):
        return sum([deposit.amount for deposit in self.flow.values()])

    def save(self, money):
        if money.start_date in self.flow:
            raise Exception("deposit (%s) duplicated" % money.start_date.strftime("%Y%m%d"))
        self.flow[money.start_date] = money

    def withdraw(self, date, amount):

        # print "amount %s" % amount
        earn = 0
        date_list = sorted(self.flow.keys(), reverse=True)
        while date_list:
            recent_date = date_list.pop(0)
            # print "recent_date %s" % recent_date.strftime("%Y%m%d")

            if recent_date >= date:
                raise Exception("recent_date(%s) is greater than date(%s)" % (
                    recent_date.strftime("%Y%m%d"), date.strftime("%Y%m%d")))

            earn += self.flow[recent_date].interest(date, amount, self.bank_rate)  # 计算利息
            withdraw_amount = self.flow[recent_date].withdraw(amount)  # 取钱

            # print "withdraw amount %s" % withdraw_amount
            amount -= withdraw_amount
            # print "amount %s" % amount
            if 0 == amount:
                break

        return earn
