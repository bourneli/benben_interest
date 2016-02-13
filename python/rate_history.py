# -*- coding: utf-8 -*-
#
# 税率历史：由于近期税率变化平凡，需要使用税率历史对象维护所有的变化
#

import ConfigParser
import datetime


#
# 每期的税率信息
#
class RateInfo:

    #
    # @param start 开始日期，格式%Y%m%d
    # @param end 结束日期，格式%Y%m%d
    # @param rates 税率信息，字典，不同时段对应的年利率
    #
    def __init__(self, rates):

        assert 'start' in rates, 'start not exist'
        assert 'end' in rates, 'end not exist '
        self._start = datetime.datetime.strptime(rates['start'], '%Y/%m/%d')
        self._end = datetime.datetime.strptime(rates['end']+" 23:59:59",  '%Y/%m/%d %H:%M:%S')

        assert 'day_1' in rates, 'day_1 not exist in %s and %s' % (self._start, self._end)
        assert 'day_7' in rates, 'day_7 not exist in %s and %s' % (self._start, self._end)
        assert 'month_3' in rates, 'month_3 not exist in %s and %s' % (self._start, self._end)
        assert 'month_6' in rates, 'month_6 not exist in %s and %s' % (self._start, self._end)
        assert 'year_1' in rates, 'year_1 not exist in %s and %s' % (self._start, self._end)
        self._rates = dict([(key, float(rates[key])) for key in rates.keys() if key in ['day_1', 'day_7', 'month_3',
                                                                                        'month_6', 'year_1']])

    def __str__(self):
        return 'From %s to %s, list:%s' % (self._start, self._end, self._rates)

    def start(self): return self._start

    def end(self): return self._end

    def rates(self): return self._rates


#
# 税率历史
#
class RateHistory:

    def __init__(self, conf):
        fr = ConfigParser.ConfigParser()
        fr.read(conf)
        self._rate_list = [RateInfo(dict(fr.items(rate_name))) for rate_name in fr.sections()]

    def get_rates(self, date):

        for rate_info in self._rate_list:
            if rate_info.start() <= date <= rate_info.end():
                print rate_info
                return rate_info.rates()

        raise Exception("Not found rates for date %s" % date)

    def __str__(self):
        return "\n".join([str(rate) for rate in self._rate_list])

if '__main__' == __name__:
    rh = RateHistory(u'配置.ini')
    print rh

    print rh.get_rates(datetime.datetime.strptime("20150101",  "%Y%m%d"))