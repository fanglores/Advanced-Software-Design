from pipe import Pipe
from typing import List
from threading import Thread

class InputFilter(Thread):
    def __init__(self, pipe_out: Pipe, lines: List[str]):
        super().__init__()
        self.pipe_out = pipe_out
        self.lines = lines

    def run(self):
        for line in self.lines:
            self.pipe_out.write(line)
        
        self.pipe_out.write(None)
