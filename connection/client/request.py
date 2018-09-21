import _socket

from connection.Command import Command


class Request:
    # call back is a method of 1 parameter
    # parameter is of type command
    def __init__(self, socket: _socket.socket, callback, command : Command):
        self.command = command
        self.callback = callback
        self.socket = socket
