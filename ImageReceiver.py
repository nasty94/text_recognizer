import socket
from connection.StreamListener import StreamListener
from Constants import SOCKET_NO
from NetworkConfig import ADDRESS
from connection.server.initializer import Initializer


class ImageReceiver:
    def __init__(self, upload_image_received_call_back):
        self.upload_image_received_call_back = upload_image_received_call_back

    def start_connection(self):
        initializer = Initializer(ADDRESS, SOCKET_NO)
        initializer.start_connection()
        initializer.set_upon_connection_call_back(self.upon_connecting)
        initializer.wait_for_connections()

    def upon_connecting(self, _socket: socket):
        stream_listener = StreamListener(_socket)
        stream_listener.set_upon_data_call_back(self.upload_image_received_call_back)
        stream_listener.start()
