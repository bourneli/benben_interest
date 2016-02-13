# -*- coding: utf-8 -*-  
#
# 程序主入口
#

import sys
import os.path
import traceback

from toolkit import *
from account import Account
from rate_history import RateHistory


#
# 加载存量数据
#
def load_balance_flow(data_file):

    file_reader = open(data_file)
    data = [line.strip().split(',') for line in file_reader.readlines() if '' != line.strip()]
    balance_list = [(datetime.datetime.strptime(d[0], "%Y/%m/%d"), int(float(d[1]))) for d in data]
    balance_list = sorted(balance_list, key=lambda item: item[0])
    assert len(balance_list) == 1 + (balance_list[-1][0] - balance_list[0][0]).days, "data length error"
    return balance_list


#
# 主入口
#
def main():

    try:

        rate_history = RateHistory(u"配置.ini")
        print rate_history
        # return

        if len(sys.argv) < 2:
            data_file = raw_input(u"请输入文件名称:".encode('gbk')).decode('gbk')
        else:
            data_file = sys.argv[1]

        if not os.path.isfile(data_file):
            print u"文件'%s'不存在" % data_file
            exit(0)

        balance_list = load_balance_flow(data_file)
        acc = Account(rate_history)
        earn = acc.interest(balance_list)

        open(u"明细.csv", "w").write(str(acc))
        print u"余额明细如下\n%s" % acc
        print u"明细可参考文档'明细.csv'"
        print u"总利息 %s亿，余额 %s亿" % (earn, acc.total_amount())
        print u"计算完成！"
    except Exception, e:
        print u"异常:%s" % str(e)
        traceback.print_tb()

    print u"按任意键结束！"
    raw_input("")


if __name__ == "__main__":
    main()
