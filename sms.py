#!C:\Python27\python.exe
#coding=utf-8

# sms
# sms sender for 2n Bluestar GSM gateway
# Copyright (C) 2015 Ilin Dmytry <ilin.dmitry279@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import sys
import telnetlib
def pdunumber(number):
    number = str(number)
    pdu_number = ''
    if '+' in number:
        number = (number[1:(len(number)-1)])
    if len(number)==11:
        number = number[1:]
    elif len(number)==12:
        number = number[2:]
    elif len(number) == 9:
        number = '0' + number
    for i in range(0,len(number)):
        if i%2==0:
            continue
        pdu_number += number[i] + number[i-1]
    return pdu_number

def convasciitoseven(text):
    ascii=[]
    eithbin=[]
    for i in text:
        ascii.append((bin(ord(i))[2:]).rjust(7,'0'))
    for i in range(len(ascii)):
        if i!=len(ascii)-1:
            if len(ascii[i])!=0:
                eithbin.append((ascii[i+1][(len(ascii[i])-1):])+ascii[i])
                ascii[i+1]=ascii[i+1][0:(len(ascii[i])-1)]
            else:
                continue
        elif ascii[i]!='':
            eithbin.append(ascii[i])
    message = (hex(len(text))[2:].rjust(2,'0')).upper()
    for i in eithbin:
        message += (hex(int(i,2))[2:].rjust(2,'0')).upper()
    return message

def isflash(flash):
    flash = str(flash)
    if flash=='0':
        return '00'
    return '10'

def csum(text):
    cs = []
    control=0x0
    for i in range(len(text)):
        if i%2==0:
            continue
        cs.append(text[i-1]+text[i])
    for i in range(len(cs)):
        control+=int(cs[i],16)
    return hex(control)[-2:]

def connector(gatemess):
    host = '172.16.0.11' # Change 172.16.0.11 on ip address of your 2n blustar gateway
    dr = []
    tn = telnetlib.Telnet(host)
    tn.write("\n\r")
    tn.read_until('SG login: ',5)
    tn.write("2n\r") # Change 2n on your login
    tn.read_until('Password: ',5)
    tn.write("2n\r") # Change 2n on your password
    tn.read_until('',5)
    tn.write("at!g=a6\r")
    answer = tn.read_until('OK',3)
    tn.write(gatemess + "\r")
    dr.append(tn.read_until('*smsout: 1,32,1',3))
    tn.write("at!g=55\r")
    tn.read_until('',3)
    tn.close()
    return dr

def logfile (dr):
    log = dr[0][2:9] + ' ' + dr[0][13:15] + ' ' + dr[0][17:]
    while log.find('\r\n') != -1:
        replnumchr = log.find('\r\n')
        log = log.replace((log[replnumchr:replnumchr+2]), ' ')
    logfile = open("smslog.txt", "a")
    from datetime import datetime
    logfile.write(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' ' + log + str(z) + '\r')
    logfile.close()
    return datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' ' + log + str(z) + '\r'

def zalyshok(sim):
    host = '172.16.0.11' # Change 172.16.0.11 on ip address of your 2n blustar gateway
    tn = telnetlib.Telnet(host)
    tn.write("\n\r")
    tn.read_until('SG login: ',5)
    tn.write("2n\r") # Change 2n on your login
    tn.read_until('Password: ',5)
    tn.write("2n\r") # Change 2n on your password
    out_ok = tn.read_until('OK',5)
    ussd112='at&g' + str(sim) + '=xtd*112#;\r'
    tn.write(ussd112)
    out_sms = tn.read_until('S;',6)
    tn.close()
    if out_sms.find('ZALYSHOK')== -1:
        global jj
        if jj < (len(check_zero())-1):
            jj += 1
            zal = zalyshok(check_zero()[jj])
        else:
            zim = check_zero()[0]
            zal = zalyshok(zim)
        while type(zal[0]) is tuple:
            zal = zal[0]
        return zal[0], zal[1]
    else:
        zal = out_sms[out_sms.find('ZALYSHOK'):-1]
        zal = zal[10:-4]
    return zal,sim

def check_zero(filyk = 'bill.py'):
    from datetime import datetime
    sim_example= ['0', '1', '2', '3', '4', '5']
    try:
        bill_r = open(filyk, 'r')
        content = bill_r.read()
        bill_r.close()
    except IOError:
        bill_a = open(filyk, 'a')
        bill_a.write(datetime.strftime(datetime.now(), "%Y%m"))
        bill_a.close()
        return sim_example
    if content.find(datetime.strftime(datetime.now(), "%Y%m")) == -1:
            bill_w = open(filyk, 'w')
            bill_w.write(datetime.strftime(datetime.now(), "%Y%m"))
            bill_w.close()
            return sim_example
    else:
        sim = content.split(' ')
        sim_for_check = [int(x) for x in sim_example if not x in sim]
        return sim_for_check

# Checking the input arguments
num = str(sys.argv[1])
mess  = str(sys.argv[2])
try: 
    flash = sys.argv[3]
except IndexError: 
    flash = '0'
# Checking SMS balance
for jj in check_zero():
    z = zalyshok(jj)
    if int(z[0]) < 10: # Мinimum balance for sending SMS
        bill_a = open('bill.py', 'a')
        bill_a.write(' ' + str(z[1]))
        bill_a.close()
    else:
        break
if len(check_zero()) == 0:
    zero_bal = "Balance of all cards is low then limit. SMS NOT SEND!"
    logfile = open("smslog.txt", "a")
    from datetime import datetime
    logfile.write(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' ' + '0001000A81' + pdunumber(num) + '00' + isflash(flash) + convasciitoseven(mess) + ' ' + zero_bal +'\r')
    logfile.close()
    print zero_bal
    sys.exit()
# PDU formation
pdumess = '0001000A81' + pdunumber(num) + '00' + isflash(flash) + convasciitoseven(mess)
lenpdumess = str(len(pdumess)/2 - 1)
gatemess = 'AT^SM=' + str(z[1]) + ',' + lenpdumess + ',' + pdumess + ',' + csum(pdumess)
# SMS sending
dr = connector(gatemess)
check = str(dr[0])
if check.find('*smsout')==-1:
    print 'SMS IS SENT ...'
    while check.find('*smsout')==-1:
        dr = connector(gatemess)
        check = str(dr[0])
print 'SMS WAS SENT'
# Logging
print logfile(dr)





