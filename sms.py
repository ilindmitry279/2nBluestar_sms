#!/usr/local/bin/python
#coding=utf-8
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
num = str(sys.argv[1])
mess  = str(sys.argv[2])
try: 
    flash = sys.argv[3]
except IndexError: 
    flash = '0'
pdumess = '0001000A81' + pdunumber(num) + '00' + isflash(flash) + convasciitoseven(mess)
lenpdumess = str(len(pdumess)/2 - 1)
gatemess = 'AT^SM=1,' + lenpdumess + ',' + pdumess + ',' + csum(pdumess)
#print gatemess
host = '172.16.0.11'
dr = []
tn = telnetlib.Telnet(host)
tn.write("\n\r")
tn.read_until('SG login: ',5)
tn.write("2n\r")
tn.read_until('Password: ',5)
tn.write("2n\r")
tn.read_until('',5)
tn.write("at!g=a6\r")
answer = tn.read_until('OK',3)
print answer
tn.write(gatemess + "\r")
dr.append(tn.read_until('*smsout: 1,32,1',3))
tn.write("at!g=55\r")
tn.read_until('',3)
tn.close()
log = dr[0][2:9] + ' ' + dr[0][13:15] + ' ' + dr[0][17:]
while log.find('\r\n') != -1:
    replnumchr = log.find('\r\n')
    log = log.replace((log[replnumchr:replnumchr+2]), ' ')
logfile = open("smslog.txt", "a")
from datetime import datetime, date, time
logfile.write(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S") + ' ' + log + '\r')
logfile.close()
print log
