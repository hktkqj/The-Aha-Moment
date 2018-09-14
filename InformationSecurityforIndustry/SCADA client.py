# !/usr/bin/python
# -*- coding : UTF-8 -*-
# File name : SCADA server.py

import socket
from EthernetSimulation import EthernetData
import threading
import random
import time

#Assume OriginAddress = 58-FB-84-8C-22-14
#Assume DestinationAddress = 5A-FB-84-8C-22-10

class RTU_PLC(object):
    def __init__(self,name,address):
        self.address = address
        self.name = name

    def package_sensor_data(self):
        data = random.randint(1, 500)
        self.__nowData = data
        self.EthernetFlash = EthernetData(self.name,self.address,data)
        return  self.EthernetFlash.Total()

    def send_data(self):
        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 10086
        s.connect((host,port))
        print(str(s.recv(1024))[2:-1])
        for i in range(1,10) :
            s.send(self.package_sensor_data().encode('utf-8'))
            print("Send: "+str(self.__nowData)+" - "+str(s.recv(1024))[2:-1])
            time.sleep(1)
        s.send('done'.encode('utf-8'))
        s.close()

if __name__ == '__main__':
    pro = RTU_PLC('58-FB-84-8C-22-14','5A-FB-84-8C-22-10')
    pro.send_data()