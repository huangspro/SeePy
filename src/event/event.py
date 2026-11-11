from abc import ABC


class Event(ABC):
    def __init__(self, name, data):
        self.name = name
        self.data = data


class ParseFailed(Event):
    def __init__(self, data):
        Event.__init__(self, "ParseFailed", data)


class ParseSuccess(Event):
    def __init__(self, data):
        Event.__init__(self, "ParseSuccess", data)
