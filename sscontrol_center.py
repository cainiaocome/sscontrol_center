#!/usr/bin/env python2.7
#encoding: utf-8

import sys
import socket
import time
import datetime
import json
import pymysql
import string
import random
import logging
import threading

import re
from prepare_database import get_not_used_transfer_record, check_user, insert_user, get_not_expired_user, get_a_free_port

logging.basicConfig(filename='log.sscontrol_center', format='%(asctime)s %(message)s', level=logging.DEBUG)

def random_string_generator(size=8, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for i in range(size))

def update_user():  # update active_user table and expired_user table
    while True:
        time.sleep(3)
        not_expired_user = get_not_expired_user()
        for x in not_expired_user:
            today = datetime.date.today()
            if today > x['expire_time']:
                force_expire_user(x['transfer_id'])
        not_used_transfer = get_not_used_transfer_record()
        for x in not_used_transfer:
            if check_user(x['transfer_id']):
                continue
            update_table_transfer_to_used(x['transfer_id'])
            transfer_id = x['transfer_id']
            server = 'jp.1isp.cc'
            port = get_a_free_port()
            password = random_string_generator()
            create_time = x['create_time']
            expired_or_not = 0
            if x['amount']==1:  # #1
                expire_time = create_time + datetime.timedelta(days=2)
            if x['amount']==15: # #2
                expire_time = create_time + datetime.timedelta(days=30)
            if x['amount']==150: # #3
                expire_time = create_time + datetime.timedelta(days=30)
        insert_user((transfer_id, server, port, password, create_time, expire_time, expired_or_not))

def main():
    thread_update_user = threading.Thread(target=update_user)
    thread_update_user.setDaemon(True)
    while True:
        time.sleep(3600)

if __name__=='__main__':
    main()
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server_address = ('0.0.0.0', 5600)
#print 'starting up on %s port %s' % server_address
#sock.bind(server_address)
#while True:
#    data,address = sock.recvfrom(65000)
#    
#    try:
#        msg = json.loads(data)
#        if not msg['password']=='alipaywatch':
#            continue
#    except:
#        print address
#        continue
#    s = bs(msg['msg'], "html.parser")
#    transfer_id = ''
#    create_time = ''
#    amount = 0

