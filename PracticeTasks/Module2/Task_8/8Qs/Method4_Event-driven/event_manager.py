import enum


class IEvents(enum.Enum):
    INITIAL_SET_EVENT = 0
    QUEEN_PLACED_EVENT = 1
    FINISHED_EVENT = 2


class EventManager:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: IEvents, subscriber):
        assert(event_type in IEvents)
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(subscriber)

    def fire(self, event_type: IEvents, data=None):
        if event_type in self.subscribers:
            for listener in self.subscribers[event_type]:
                listener() if data is None else listener(data)
