import jsonpickle
import json


class Command:
    def __init__(self, code="", data=""):
        self.code = code
        self.data = data

    @staticmethod
    def from_string(string: str):
        return Command(**jsonpickle.decode(string))

    def __str__(self):
        return jsonpickle.encode(self, unpicklable=False)
