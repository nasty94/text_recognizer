from connection.Command import Command
from connection.client.request import Request
from connection.singleton import Singleton

# ignore for now till using multi threads
# noinspection PyMethodMayBeStatic
@Singleton
class CommandExecutor:
    # TODO
    def add_request(self, request: Request):
        request.socket.send(str(request.command).encode())
        respond = request.socket.recv(4096).decode()
        if respond == "" or respond is None:
            return
        request.callback(Command.from_string(respond))

