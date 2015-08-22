#!/usr/local/bin/python
#coding=utf-8
def check_zero(filyk = 'bill.py'):
    from datetime import datetime
    #import pdb; pdb.set_trace()
    filyk = 'bill.py'
    sim_example= ['0', '1', '2', '3', '4', '5']
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
        sim_for_check = [int(x) for x in sim_example if not x in sim]
        return sim_for_check