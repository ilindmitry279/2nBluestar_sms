#!/usr/local/bin/python
#coding=utf-8
def check_zero():
    from datetime import datetime
    filyk = 'bill.py'
    sim_example= ['00', '01', '02', '03', '04', '05']
    try:
        bill_r = open(filyk, 'r')
        content = bill_r.read()
        bill_r.close()
    except IOError:
        bill_a = open(filyk, 'a')
        bill_a.write(datetime.strftime(datetime.now(), "%Y%m") + ' ')
        bill_a.close()
        return sim_example
    if content.find(datetime.strftime(datetime.now(), "%Y%m")) == -1:
            bill_w = open(filyk, 'w')
            bill_w.write(datetime.strftime(datetime.now(), "%Y%m") + ' ')
            bill_w.close()
            return sim_example
    else:
        sim = content.split(' ')
        sim_for_check = [x for x in sim_example if not x in sim]
        return sim_for_check