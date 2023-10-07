import socket



class AutomatedTankGauge:
    def __init__(self, address):
        self.address = address
        self.data = []


    def netcat(hostname, port, content):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        s.sendall(content)
        s.shutdown(socket.SHUT_WR)
        while 1:
            data = s.recv(1024)
            if len(data) == 0:
                break
            print("Received:", repr(data))
        print("Connection closed.")
        s.close()
