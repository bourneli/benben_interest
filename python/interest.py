# -*- coding: utf-8 -*-  

import datetime
import calendar
import sys
import os.path
import ConfigParser


# BANK_RATE = {"year_1":0.05,
# "month_6":0.045,
# "month_3":0.040,
# "day_7":0.020,
# "day_1":0.010}



def add_months(baseTime, offset):
    # 获取年，月，日
    year = int(str(baseTime)[0:4])
    month = int(str(baseTime)[4:6])
    day = int(str(baseTime)[6:8])

    # 对月份和偏移月数加和后的特殊情况进行处理
    if 0 == (month + offset) % 12:
        yearOffset = (month + offset) / 12 - 1
        monthOffset = 12
    else:
        yearOffset = (month + offset) / 12
        monthOffset = (month + offset) % 12

    targetMonth = monthOffset
    targetYear = year + yearOffset

    # 将转换后的日进行合法化
    lastDayOfMonth = calendar.monthrange(targetYear, targetMonth)[1]
    targetDay = day < lastDayOfMonth and day or lastDayOfMonth

    # 转换
    convertedTime = datetime.datetime(targetYear, targetMonth, targetDay)
    targetTime = convertedTime.strftime("%Y%m%d")
    return targetTime


def add_months_obj(date_obj, months):
    return datetime.datetime.strptime(add_months(date_obj.strftime("%Y%m%d"), months), "%Y%m%d")


def diff_year(from_date, to_date):
    return int(diff_month(from_date, to_date) / 12)


def diff_month(from_date, to_date):
    if from_date > to_date:
        raise Exception("from_date(%s) is greater than to_date (%s)" % (
        from_date.strftime("%Y-%m-%d %H:%M:%S"), to_date.strftime("%Y-%m-%d %H:%M:%S")))

    diff = 0
    current_date = from_date
    while True:
        # print current_date.strftime("%Y%m%d")
        current_date = datetime.datetime.strptime(add_months(current_date.strftime("%Y%m%d"), 1), "%Y%m%d")
        if current_date > to_date:
            break
        diff += 1

    # print "diff %s" % diff
    return diff


class NatureDateDiff:
    def diff(self, start_date, statis_date):
        diff_year_1 = diff_year(start_date, statis_date)

        current_date = add_months_obj(statis_date, -12 * diff_year_1)
        diff_month_6 = diff_month(start_date, current_date) / 6

        current_date = add_months_obj(current_date, -6 * diff_month_6)
        diff_month_3 = diff_month(start_date, current_date) / 3

        current_date = add_months_obj(current_date, -3 * diff_month_3)
        diff_day_7 = (current_date - start_date).days / 7

        current_date -= datetime.timedelta(days=7 * diff_day_7)
        diff_day_1 = (current_date - start_date).days

        return (diff_year_1, diff_month_6, diff_month_3, diff_day_7, diff_day_1)


class StrictDateDiff:
    def split(self, amount, base):
        # print "StrictDateDiff"
        count = int(amount / base)
        rest = amount - count * base
        return (count, rest)

    def diff(self, start_date, statis_date):
        # start_date = datetime.datetime.strptime(start_date, "%Y%m%d")
        # statis_date = datetime.datetime.strptime(statis_date, "%Y%m%d")

        diff_days = (statis_date - start_date).days
        (diff_year_1, diff_days) = self.split(diff_days, 365)
        (diff_month_6, diff_days) = self.split(diff_days, 365 / 2)
        (diff_month_3, diff_days) = self.split(diff_days, 365 / 4)
        (diff_day_7, diff_days) = self.split(diff_days, 7)
        (diff_day_1, diff_days) = self.split(diff_days, 1)

        return (diff_year_1, diff_month_6, diff_month_3, diff_day_7, diff_day_1)


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
            diff_day_7 * rate_map["day_7"] * (7 / 365.0) +
            diff_day_1 * rate_map["day_1"] * (1 / 365.0))


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


def main():
    try:

        confReader = ConfigParser.ConfigParser()
        confReader.read(u"配置.ini")
        print confReader.sections(), confReader.options("interest_rate")
        BANK_RATE = {"year_1": confReader.getfloat("interest_rate", "year_1"),
                     "month_6": confReader.getfloat("interest_rate", "month_6"),
                     "month_3": confReader.getfloat("interest_rate", "month_3"),
                     "day_7": confReader.getfloat("interest_rate", "day_7"),
                     "day_1": confReader.getfloat("interest_rate", "day_1")}
        print BANK_RATE

        data_file = ''
        mode = ''
        if len(sys.argv) < 2:
            data_file = raw_input(u"请输入文件名称:".encode('gbk')).decode('gbk')
            mode = raw_input(u"请输计算类型，‘s’表示严格理论，‘n’表示自然月利率:".encode('gbk')).decode('gbk')
        else:
            data_file = sys.argv[1]
            mode = sys.argv[2].strip().lower() if len(sys.argv) > 2 else ""

        mode = "strict" if "s" == mode else "nature"
        if not os.path.isfile(data_file):
            print u"文件'%s'不存在" % data_file
            exit(0)

        if "nature" == mode:
            print u"自然月计算 ", mode
        else:
            print u"严格计算 ", mode

        file = open(data_file)
        data = [line.strip().split(",") for line in file.readlines() if '' != line.strip()]
        storage_list = [(datetime.datetime.strptime(d[0], "%Y/%m/%d"), int(float(d[1]))) for d in data]
        storage_list = sorted(storage_list, key=lambda item: item[0])

        acc = Account(BANK_RATE)
        if storage_list:
            inital_storage = storage_list.pop(0)
            acc.save(Deposit(inital_storage[0], inital_storage[1], mode))
        # print acc

        earn = 0.0
        for storage in storage_list:
            (storage_date, storage_amount) = storage
            total_amount = acc.total_amount()
            # print "total_amount %d" % total_amount

            if storage_amount > total_amount:
                acc.save(Deposit(storage_date, storage_amount - total_amount, mode))
            elif storage_amount < total_amount:
                earn += acc.withdraw(storage_date, total_amount - storage_amount)

        print u"总利息 %s亿，余额 %s亿，\n下面是余额明细:" % (earn, acc.total_amount())
        # print acc
        open(u"明细.csv", "w").write(str(acc))
    except Exception, e:
        print u"异常:%s" % str(e)

    print u"计算完成！"
    raw_input("")


def test():
    print add_months(20140131, 1)
    print add_months(20140228, -1)


if __name__ == "__main__":
    main()
    # test()
