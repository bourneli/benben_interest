# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import random

start = datetime.strptime('20140301', '%Y%m%d')
end = datetime.strptime('20151212', '%Y%m%d')

n = (end-start).days + 1

random.seed(3474)
test_data = [(start + timedelta(days=i), 10 + random.random()*20) for i in xrange(0, n)]
raw_data = '\n'.join(['%s,%.1f' % (date.strftime('%Y/%m/%d'), amount)
                      for date, amount in test_data])
print raw_data

fd = open('../data/test_rate.txt', 'w')
fd.write(raw_data)
fd.close()
print "Complete"