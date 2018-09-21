from socket import *


class Initializer:
    def __init__(self, address: str, port: int):
        self.port = port
        self.socket = socket()
        self.call_backs = []
        self.address = address

    def start_connection(self):
        self.socket.bind((self.address, self.port))
        self.socket.listen(5)

    def wait_for_connections(self):
        while True:
            client_socket, _ = self.socket.accept()
            self.__on_client_connection(client_socket)

    def __on_client_connection(self, m_socket):
        for call_back in self.call_backs:
            call_back(m_socket)

    def set_upon_connection_call_back(self, call_back):
        """
        :param call_back: function of one parameter f(socket)
        """
        self.call_backs.append(call_back)
