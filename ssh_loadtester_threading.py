#!/usr/local/bin/python3

import sys, os, string, threading
import paramiko
import json

lock = threading.Lock()

def main():
    threads = []
    # host = input("Enter proxy IP: ")
    # port = input("Enter proxy port: ")
    # load = input("Enter number of connections: ")
    # sleeptime = input("Enter sleeptime (seconds): ")
    with open('loadtest.json', 'r') as f:
        loadtest_config = json.load(f)
    host = loadtest_config['host']
    port = loadtest_config['port']
    load = loadtest_config['load']
    sleeptime = loadtest_config['sleeptime']

    #host, port = '172.16.171.132', 8022
    #run = "echo hi; sleep 10"
    run = "echo hi; sleep " + str(sleeptime)
    for _ in range(load):
        thread = threading.Thread(target=sshRun, args=(host, port, run))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    

def sshRun(host,port,run):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username='test', password='test')
    stdin, stdout, stderr = ssh.exec_command(run)
    stdin.write('xy\n')
    stdin.flush()
    with lock:
        _ = stdout.readlines()

if __name__ == "__main__":
    main()