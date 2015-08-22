#!/usr/local/bin/python
#coding=utf-8
import telnetlib
def zalyshok(sim):
    host = '172.16.0.11'
    tn = telnetlib.Telnet(host)
    tn.write("\n\r")
    tn.read_until('SG login: ',5)
    tn.write("2n\r")
    tn.read_until('Password: ',5)
    tn.write("2n\r")
    out_ok = tn.read_until('OK',5)
    ussd112='at&g' + str(sim) + '=xtd*112#;\r'
    tn.write(ussd112)
    out_sms = tn.read_until('S;',6)
    tn.close()
    if out_sms.find('ZALYSHOK')== -1:
        sim_n = sim
        if sim_n < 5:
            sim_n += 1
            print sim_n
            zal = zalyshok(sim_n)
        else:
            print check_zero()[0]
            zim = check_zero()[0]
            zal = zalyshok(zim)
    else:
        zal = out_sms[out_sms.find('ZALYSHOK'):-1]
        zal = zal[10:-4]
    while type(zal[0]) is tuple:
        zal = zal[0]
    return zal,sim