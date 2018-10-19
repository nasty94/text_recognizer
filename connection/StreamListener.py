import threading
from socket import *

import struct


class StreamListener(threading.Thread):
    def __init__(self, m_socket: socket):
        """
        Listen on socket for stream connection
        upon connection the client should send the meta data
        the meta data format is as following:

        size: value\n
        param1:value\n
        param2:value\n
        ...
        paramN:value\r\n\

        NOTEs:
         1- the parameters MUST contain size other than that connection will be terminated
         2- the parameters must be separated with \n
         3- the last parameter must end with \n\n\r
         4- all the meta data will return in the callbacks as dict of key and value
        :param m_socket: the socket where the StreamListener will continue listening to
        """
        threading.Thread.__init__(self, name="connection Listener")
        self.socket = m_socket
        self.call_backs = []

    def set_upon_data_call_back(self, call_back):
        """
        this callbacks are triggered whenever data comes from remote
        :param call_back: function of three parameter f(byte[], metaData: dict , socket)
        """
        self.call_backs.append(call_back)

    def run(self):

        # try:
            buff_size = 8
            meta_data = StreamListener.__parse_meta_data(self.__receive_meta_data())
            size = int(meta_data["size"])
            size -= buff_size
            arr = self.socket.recv(buff_size)
            while buff_size:
                arr += self.socket.recv(buff_size)
                size -= buff_size
                buff_size = size if size < buff_size else buff_size
            self.__trigger_call_backs(bytearray(arr), meta_data)

        # except Exception as ex:
        #     # TODO return this exception to the user
        #     print(ex)

    def __trigger_call_backs(self, file, metadata: dict):
        for call_back in self.call_backs:
            call_back(file, metadata, self.socket)

    def __receive_meta_data(self):
        end_of_text = 0
        text = ""
        while end_of_text != 2:
            buffer = self.socket.recv(1).decode()
            if buffer == '\r':
                end_of_text = 1
            elif end_of_text != 0 and buffer == '\n':
                end_of_text = 2
            else:
                text += buffer
        return text

    @staticmethod
    def __parse_meta_data(text : str):
        text.replace(" ", "")
        lines = text.split("\n")
        meta_data = dict()
        for line in lines:
            key, value = line.split(":")
            meta_data[key] = value
        return meta_data
