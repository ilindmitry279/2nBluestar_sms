#!/usr/local/bin/python
#coding=utf-8
import telnetlib#(sim)
sim='03'
host = '172.16.0.11'
dr = []
tn = telnetlib.Telnet(host)
tn.write("\n\r")
tn.read_until('SG login: ',5)
tn.write("2n\r")
tn.read_until('Password: ',5)
tn.write("2n\r")
out_ok = tn.read_until('OK',5)
ussd112='at&g' + sim + '=xtd*112#;\r'
tn.write(ussd112)
out_sms = tn.read_until('S;',6)
tn.close()
print len(out_sms)
print out_sms
