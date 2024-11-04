from pipe import Pipe
from threading import Thread

class AlphabetizerFilter(Thread):
    def __init__(self, pipe_in: Pipe, pipe_out: Pipe):
        super().__init__()
        self.pipe_in = pipe_in
        self.pipe_out = pipe_out
        self.lines = []

    def run(self):
        while True:
            line = self.pipe_in.read()
            if line is None:
                self.lines.sort()
                for sorted_line in self.lines:
                    self.pipe_out.write(sorted_line)
                self.pipe_out.write(None)
                break
            self.lines.append(line)
