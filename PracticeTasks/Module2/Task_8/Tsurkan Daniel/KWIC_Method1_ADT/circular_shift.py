class CircularShift:
    def __init__(self, line, offset):
        self.line = line
        self.offset = offset

    def get_shifted_line(self):
        words = self.line.split()
        shifted = ' '.join(words[(self.offset + i) % len(words)] for i in range(len(words)))
        return shifted

    def __str__(self):
        return self.get_shifted_line()
