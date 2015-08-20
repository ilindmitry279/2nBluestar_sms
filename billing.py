#!/usr/local/bin/python
#coding=utf-8

def zalyshok(sim):
    #import pdb; pdb.set_trace()
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
        sim_n = int(sim)
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
    return zal