# -*- coding: utf-8 -*-  
#
# 程序主入口
#

import sys
import os.path
import ConfigParser

from toolkit import *
from account import Account
from deposit import Deposit


def main():

    try:

        conf_reader = ConfigParser.ConfigParser()
        conf_reader.read(u"配置.ini")
        rate_list = [dict(conf_reader.items(rate_name)) for rate_name in conf_reader.sections()]
        print rate_list

        if len(sys.argv) < 2:
            data_file = raw_input(u"请输入文件名称:".encode('gbk')).decode('gbk')
        else:
            data_file = sys.argv[1]

        if not os.path.isfile(data_file):
            print u"文件'%s'不存在" % data_file
            exit(0)

        file_reader = open(data_file)
        data = [line.strip().split(',') for line in file_reader.readlines() if '' != line.strip()]
        storage_list = [(datetime.datetime.strptime(d[0], "%Y/%m/%d"), int(float(d[1]))) for d in data]
        storage_list = sorted(storage_list, key=lambda item: item[0])

        acc = Account(rate_list)
        earn = 0.0
        for storage_date, storage_amount in storage_list:
            total_amount = acc.total_amount()

            # 计算当前的存量
            if storage_amount > total_amount:
                acc.save(Deposit(storage_date, storage_amount - total_amount))
            elif storage_amount < total_amount:
                earn += acc.withdraw(storage_date, total_amount - storage_amount)

            # 取出一年前的数据，计算利息，并且存到明天的账号中
            earn += acc.cycle(storage_date)
            # print storage_date

        open(u"明细.csv", "w").write(str(acc))
        print u"余额明细如下\n%s" % acc
        print u"明细可参考文档'明细.csv'"
        print u"总利息 %s亿，余额 %s亿" % (earn, acc.total_amount())
        print u"计算完成！"
    except Exception, e:
        print u"异常:%s" % str(e)

    print u"按任意键结束！"
    raw_input("")


if __name__ == "__main__":
    main()
