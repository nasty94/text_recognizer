from _socket import socket


# in order to add multiple listeners
class Connection:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = socket()

    def start_connection(self):
        self.socket.connect((self.address, self.port))
