from abc import ABC


class Event(ABC):
    def __init__(self, name, data):
        self.name = name
        self.data = data


class ParseFailed(Event):
    def __init__(self, data):
        Event.__init__(self, "ParseFailed", data)


class OnStart(Event):
    def __init__(self, data):
        Event.__init__(self, "OnStart", data)


class ParseSuccess(Event):
    def __init__(self, data):
        Event.__init__(self, "ParseSuccess", data)


class UIPrepared(Event):
    def __init__(self, data):
        Event.__init__(self, "UIPrepared", data)


class TargetNotFound(Event):
    def __init__(self, data):
        Event.__init__(self, "TargetNotFound", data)


class ChartChanged(Event):
    def __init__(self, data):
        Event.__init__(self, "ChartChanged", data)


class ChartPrepared(Event):
    def __init__(self, data):
        Event.__init__(self, "ChartPrepared", data)
