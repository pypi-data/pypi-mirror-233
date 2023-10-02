# -*- coding: utf-8 -*-
"""
Created on Sun May 21 11:24:03 2023

@author: neurobrave
"""

import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    value = json.loads(data,'utf-8')["relaxation"]
    print("received message: %s" % data)
    print("received message: %s" % data)
    