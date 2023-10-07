import csv
import os
import ipaddress
import socket
from urllib import request





class Record:
    def __init__(self, path):
        self.path = path

    def store(sensor):
        with open(os.path.join(self.path, sensor.address + ".csv"), "a") as f:
            f.write(sensor + "," + str(open_ips) + "\n")


class Sensor:
    def __init__(self, address, port, method):
        self.address = address
        self.port = port
        self.method = method
    
    def scan(self):
        socket.setdefaulttimeout(2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            con = s.connect((self.address,self.port))
            con.close()
            return True
        except:
            return False

    @abstractmethod
    def get_data(self):
        if (self.method == 'http'):
            # send http request to address on port and save response
            return request.get(self.address)


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
    # find all rows with target zip in column 8
    ips = []
    for row in data:
        if row[8] == zip:
            for i in range(int(row[0]), int(row[1])):
                ips.append(long2DotIP(i))
    return ips


def scanIPs(ips, port):
    open_ips = []
    if (ips == None):
        return []
    for ip in ips:
        socket.setdefaulttimeout(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip,port))
        if result == 0:
            print("Port " + str(port) + " is open on " + ip)
            open_ips.append(ip)
        sock.close()
    return open_ips



if __name__ == "__main__":
    data = loadCSV()
    zip = '60540'
    port = 8080
    print("Getting IPs within ZIP code: " + zip)
    ips = getIPs(data, zip)
    print("Scanning IPs for port: " + str(port))
    open_ips = scanIPs(ips, port)
