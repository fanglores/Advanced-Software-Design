from queue import Queue

class Pipe:
    def __init__(self):
        self.data = Queue()

    def write(self, value):
        self.data.put(value)

    def read(self):
        return self.data.get()
    
    def has_data(self):
        return not self.data.empty()
