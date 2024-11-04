# circular_shift_filter.py
from pipe import Pipe
from threading import Thread

class CircularShiftFilter(Thread):
    def __init__(self, pipe_in: Pipe, pipe_out: Pipe):
        super().__init__()
        self.pipe_in = pipe_in
        self.pipe_out = pipe_out

    def run(self):
        while True:
            line = self.pipe_in.read()
            if line is None:
                self.pipe_out.write(None)
                break
            words = line.split()
            for i in range(len(words)):
                shifted_line = ' '.join(words[i:] + words[:i])
                self.pipe_out.write(shifted_line)
