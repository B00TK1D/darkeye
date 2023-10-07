from abc import abstractmethod
import threading
from queue import Queue
import time
import socket
import csv
import os
import ipaddress
from urllib import request



portscan_lock = threading.Lock()

q = Queue()

port = 80

open_ips = []







def portscan(target, port):
    socket.setdefaulttimeout(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target,port))
        with portscan_lock:
            print('Port ', port, ' is open on ', target)
            open_ips.append(target)
        con.close()
    except:
        pass


def threader():
    while True:
        worker = q.get()
        portscan(worker, port)
        q.task_done()




def dot2LongIP(ip):
    return int(ipaddress.IPv4Address(ip))

def long2DotIP(ipnum):
    return str(int(ipnum / 16777216) % 256) + "." + str(int(ipnum / 65536) % 256) + "." + str(int(ipnum / 256) % 256) + "." + str(ipnum % 256)


def loadCSV():
    # open csv file as list
    print("Loading CSV file...")
    with open(os.path.join('db', 'IP2LOCATION-LITE-DB11.CSV'), 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    print("CSV file loaded.")
    return data


def getIPs(data, zip):
    ips = []
    for row in data:
        if row[8] == zip:
            for i in range(int(row[0]), int(row[1])):
                ips.append(long2DotIP(i))
    return ips


def scanIPs(ips, port):
    print("Starting threads...")
    for i in range(5000):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for ip in ips:    
        q.put(ip)

    q.join()



if __name__ == '__main__':
    data = loadCSV()
    zip = '50310'
    port = 80
    print("Getting IPs within ZIP code: " + zip)
    ips = getIPs(data, zip)
    print("Scanning " + str(len(ips)) + " IPs for port: " + str(port))
    scanIPs(ips, port)
    print(open_ips)

