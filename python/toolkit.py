# -*- coding: utf-8 -*-

import calendar
import datetime

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
    return datetime.datetime.strptime(add_months(date_obj.strftime("%Y%m%d"),
                                                 months), "%Y%m%d")


