import enum


class IEvents(enum.Enum):
    TEXT_READ_EVENT = 1
    CONTEXT_READY_EVENT = 2
    DISPLAY_CONTEXT_EVENT = 3


class EventManager:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: IEvents, subscriber):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(subscriber)

    def fire(self, event_type: IEvents, data):
        if event_type in self.subscribers:
            for listener in self.subscribers[event_type]:
                listener(data)
