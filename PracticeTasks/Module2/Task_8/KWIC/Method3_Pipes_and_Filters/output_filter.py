from pipe import Pipe
from threading import Thread

class OutputFilter(Thread):
    def __init__(self, pipe_in: Pipe):
        super().__init__()
        self.pipe_in = pipe_in

    def run(self):
        while True:
            line = self.pipe_in.read()
            if line is None:
                break
            print(line)
