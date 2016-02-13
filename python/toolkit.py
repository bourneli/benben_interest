# -*- coding: utf-8 -*-
#
# 工具模块
#
import calendar
import datetime


def add_months(base_time, offset):

    # 获取年，月，日
    year = int(str(base_time)[0:4])
    month = int(str(base_time)[4:6])
    day = int(str(base_time)[6:8])

    # 对月份和偏移月数加和后的特殊情况进行处理
    if 0 == (month + offset) % 12:
        year_offset = (month + offset) / 12 - 1
        month_offset = 12
    else:
        year_offset = (month + offset) / 12
        month_offset = (month + offset) % 12

    target_month = month_offset
    target_year = year + year_offset

    # 将转换后的日进行合法化
    last_day_of_month = calendar.monthrange(target_year, target_month)[1]
    target_day = day < last_day_of_month and day or last_day_of_month

    # 转换
    converted_time = datetime.datetime(target_year, target_month, target_day)
    target_time = converted_time.strftime("%Y%m%d")
    return target_time


def add_months_obj(date_obj, months):
    return datetime.datetime.strptime(add_months(date_obj.strftime("%Y%m%d"),
                                                 months), "%Y%m%d")


if '__main__' == __name__:
    print add_months(20160229, -36)