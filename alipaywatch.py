#!/usr/bin/env python2.7
#encoding: utf-8

import sys
import socket
import time
import json
import pymysql

import re
from bs4 import BeautifulSoup as bs

from prepare_database import check_and_insert_transfer_record

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 5599)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    print 'waiting to receive message....'
    print '-'*90
    data,address = sock.recvfrom(65000)
    
    try:
        msg = json.loads(data)
        if not msg['password']=='alipaywatch':
            continue
    except:
        print address
        continue
    s = bs(msg['msg'], "html.parser")
    transfer_id = ''
    create_time = ''
    amount = 0
    try:
        for x in s.find_all(name='tr', id=re.compile('^J-item-')):
            # transfer_id
            y = x.find(name='td', class_=re.compile('^tradeNo'))
            transfer_id = y.p.string.strip()
            transfer_id = transfer_id.split(':')[1]   # well, last result is like: 流水号:20151120200040011100920074867393
            # create_time
            y = x.find(name='p', class_='time-d')
            create_time = y.string.strip().replace('.','')
            # amount
            y = x.find(name='span', class_='amount-pay-in')
            amount = int(float(y.string.strip('+ ')))
            print 'going to check_and_insert_transfer_record', transfer_id, create_time, amount
            check_and_insert_transfer_record(transfer_id, create_time, amount)
            print '*'*90
    except:
        continue
