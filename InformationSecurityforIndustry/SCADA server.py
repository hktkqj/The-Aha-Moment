# !/usr/bin/python
# -*- coding : UTF-8 -*-
# File name : SCADA server.py

import socket
from EthernetSimulation import EthernetDataDecoder
import threading
import random
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
port = 10086
s.bind((hostname,port))
s.listen(5)

def tcplink(sock, addr):
    print ('New connection accepted...')
    sock.send("Connected".encode('utf-8'))
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if str(data)[2:-1] == 'done' :
            break
        sock.send(('Data received.').encode('utf-8'))
        print("Data received : " ,end='')
        Decoder = EthernetDataDecoder(str(data)[2:-1])
        Decoder.PrintDetails()

    sock.close()
    print('Connection closed.')

while True :
    sock, addr = s.accept()
    NewThread = threading.Thread(target=tcplink, args=(sock,addr))
    NewThread.start()