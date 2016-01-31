# -*- coding: utf-8 -*-  

import datetime
import sys
import os.path
import ConfigParser
from toolkit import *
from account import Account
from deposit import Deposit

# BANK_RATE = {"year_1":0.05,
# "month_6":0.045,
# "month_3":0.040,
# "day_7":0.020,
# "day_1":0.010}


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
