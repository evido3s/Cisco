#!/usr/bin/env python3
import paramiko
from sys import argv
import re
"""
import sqlite3

conn = sqlite3.connect("../webapp/users.db")
cred = conn.execute("select username,password from conn_user").fetchall()[0]
username, password = cred[0], cred[1]
"""
host, command = argv[1], argv[2]
hosts = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host)

def cisco_conn(host, command):
    ssh_conn = paramiko.SSHClient()
    ssh_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_conn.connect(host,
                username='cisco',
                password='cisco',
                timeout=10,
                look_for_keys=False,
                allow_agent=False)

    stdin, stdout, stderr = ssh_conn.exec_command(command)
    for i in stdout.readlines():
        print(i.rstrip())

for host in hosts:
    host = host.strip(" ")
    print('------------------------------------', host,  "-----------------------------------" )
    cisco_conn(host, command)
    print(' ')
    print(' ')
    print(' ')
    print(' ')

