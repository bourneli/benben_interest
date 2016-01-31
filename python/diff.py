# -*- coding: utf-8 -*-


from toolkit import *

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

    def __init__(self):
        pass

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

        return diff_year_1, diff_month_6, diff_month_3, diff_day_7, diff_day_1


class StrictDateDiff:

    def __init__(self):
        pass

    @staticmethod
    def split(amount, base):
        count = int(amount / base)
        rest = amount - count * base
        return count, rest

    def diff(self, start_date, statis_date):

        diff_days = (statis_date - start_date).days
        (diff_year_1, diff_days) = split(diff_days, 365)
        (diff_month_6, diff_days) = split(diff_days, 365 / 2)
        (diff_month_3, diff_days) = split(diff_days, 365 / 4)
        (diff_day_7, diff_days) = split(diff_days, 7)
        (diff_day_1, diff_days) = split(diff_days, 1)

        return diff_year_1, diff_month_6, diff_month_3, diff_day_7, diff_day_1

