import threading
from socket import *

from connection.Command import Command


class ConnectionListener(threading.Thread):
    def __init__(self, m_socket: socket):
        threading.Thread.__init__(self, name="connection Listener")
        self.socket = m_socket
        self.call_backs = []

    # this callbacks are triggered whenever data come from remote
    # callbacks should be a function with one parameter
    # parameter: is instance of command class
    def set_upon_data_call_back(self, call_back):
        """
        :param call_back: function of two parameter f(command, socket)
        """
        self.call_backs.append(call_back)

    def run(self):
        while True:
            try:
                command = Command.from_string(self.socket.recv(1024).decode())
                # TODO
                self.__trigger_call_backs(command)
            except Exception as ex:
                print(ex)
                break

    def __trigger_call_backs(self, command):
        for call_back in self.call_backs:
            call_back(command, self.socket)
