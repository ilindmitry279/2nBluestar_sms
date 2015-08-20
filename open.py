#!/usr/local/bin/python
#coding=utf-8
from datetime import datetime
filyk = 'bill.py'
sim = []
try:
    bill_r = open(filyk, 'r')
    content = bill_r.read()
    bill_r.close()
except IOError:
    bill_a = open(filyk, 'a')
    bill_a.write(datetime.strftime(datetime.now(), "%Y%m") + '\n')
    bill_a.close()
if content.find(datetime.strftime(datetime.now(), "%Y%m")) == -1:
        bill_w = open(filyk, 'w')
        bill_w.write(datetime.strftime(datetime.now(), "%Y%m") + '\n')
        bill_w.close()
    else:
        






'''print len(content)
stroka = {}
for i in range(len(content)):
    stroka[i] = content[i]
print stroka
bill_a = open(filyk, 'a')
bill_a.write('03' + '\n')
bill_a.close()'''
