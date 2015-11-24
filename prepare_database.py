#!/usr/bin/env python2.7
# encoding: utf-8

import pymysql
from config import DB_HOST, DB_USER, DB_PASS

create_table_transfer = '''
create table if not exists transfer
(
    transfer_id varchar(64),
    create_time date,
    amount int,
    used_or_not boolean default 0,
    primary key (transfer_id)
)
'''
sql_get_not_used_transfer_record = '''
select * from transfer where used_or_not=0
'''
def get_not_used_transfer_record():
    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor(pymysql.cursors.DictCursor)
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute(sql_get_not_used_transfer_record)
    data = dbcurr.fetchall()
    dbconn.commit()
    dbconn.close()
    
    return data

check_transfer_record = '''
select * from transfer where transfer_id="{}"
'''
insert_record = '''
insert ignore into transfer (transfer_id, create_time, amount) values ("{}", "{}", {})
'''
def check_and_insert_transfer_record(transfer_id, create_time, amount):

    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor()
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute(check_transfer_record.format(transfer_id))
    if dbcurr.rowcount==0:
        dbcurr.execute(insert_record.format(transfer_id, create_time, amount)) 
        print 'inserted into transfer {} {} {}'.format(transfer_id, create_time, amount)
    else:
        data = dbcurr.fetchall()
        for x in data:
            print 'record exist:', x
    dbconn.commit()
    dbconn.close()

sql_update_table_transfer_to_used = '''
update transfer set used_or_not=1 where transfer_id="%s"
'''
def update_table_transfer_to_used(transfer_id):
    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor(pymysql.cursors.DictCursor)
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute(sql_update_table_transfer_to_used, (transfer_id))
    dbconn.commit()
    dbconn.close()
    
create_table_user = '''
create table if not exists user
(
    transfer_id varchar(64),
    server varchar(64),
    port int,
    password varchar(32),

    create_time date,
    expire_time date,
    expired_or_not boolean default 0,

    primary key (transfer_id)
)
'''
def force_expire_user(transfer_id):
    sql_force_expire_user = '''
    update user set expired_or_not=1 where transfer_id="%s"
    '''
    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor(pymysql.cursors.DictCursor)
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute(sql_get_not_expired_user, (transfer_id))
    dbconn.commit()
    dbconn.close()

def get_not_expired_user():
    sql_get_not_expired_user = '''
    select * from user where expired_or_not=0
    '''
    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor(pymysql.cursors.DictCursor)
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute(sql_get_not_expired_user)
    data = dbcurr.fetchall()
    dbconn.commit()
    dbconn.close()

    return data
    
def insert_user(record):
    sql_insert_user = '''
    insert into user(transfer_id, server, port, password, create_time, expire_time, expired_or_not)
    values("%s", "%s", %d, "%s", "%s", "%s", %d)
    '''
    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor(pymysql.cursors.DictCursor)
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute(sql_insert_user, record)
    dbconn.commit()
    dbconn.close()

def check_user(transfer_id):
    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor(pymysql.cursors.DictCursor)
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute('select * from user where transfer_id="%s"', (transfer_id))
    exist_or_not = dbcurr.rowcount
    dbconn.commit()
    dbconn.close()

    return exist_or_not

def get_a_free_port():
    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor(pymysql.cursors.DictCursor)
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute('select * from user where expired_or_not=0')
    data = dbcurr.fetchall()
    dbconn.commit()
    dbconn.close()
    used_ports = list()
    for x in data:
        used_ports.append(x['port'])
    for port in range(1025,65000):
        if port not in used_ports:
            break
    return port
    
create_table_server = '''
create table if not exists server
(
    ip varchar(64),
    users varchar(1024),

    primary key (ip)
)
'''

def main():
    dbconn = pymysql.connect(DB_HOST, DB_USER, DB_PASS, 'vpn', charset='utf8')
    dbconn.autocommit(False)
    dbcurr = dbconn.cursor(pymysql.cursors.DictCursor)
    dbcurr.execute('SET NAMES utf8')

    dbcurr.execute(create_table_transfer)
    dbcurr.execute(create_table_user)
    dbcurr.execute(create_table_server)
    dbconn.commit()
    dbconn.close()
    
if __name__=='__main__':
    main()
