"""
Grace Lombardi
I made a program that sends 100 packets to a chosen IP address and portjj
"""

import socket
import random
def ping():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1362)
    ip = input('Target IP: ')
    sent = 0
    i = 100
    while i >= 0:
        sock.sendto(bytes,(ip,53))
        print("Sent %s amount of packets to %s at port %s." % (sent, ip, 53))
        sent = sent + 1
        i = i-1
