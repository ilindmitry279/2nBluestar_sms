#!/usr/local/bin/python
#coding=utf-8
def zalyshok(sim):
    sim_s = str(sim)
    import telnetlib
    host = '172.16.0.11'
    dr = []
    tn = telnetlib.Telnet(host)
    tn.write("\n\r")
    tn.read_until('SG login: ',5)
    tn.write("2n\r")
    tn.read_until('Password: ',5)
    tn.write("2n\r")
    out_ok = tn.read_until('OK',5)
    ussd112='at&g' + sim_s + '=xtd*112#;\r'
    tn.write(ussd112)
    out_sms = tn.read_until('S;',6)
    tn.close()
    if out_sms.find('ZALYSHOK')== -1:
        sim_n = sim
        if sim_n < 6:
            sim_n += 1
            zalyshok(sim_n)
        else:
            zalyshok (open())
    zal = out_sms[out_sms.find('ZALYSHOK'):-1]
    zal = zal[10:-4]
    return zal