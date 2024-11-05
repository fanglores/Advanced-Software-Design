class FindQueenPositionImpl:
    def __init__(self, queens):
        self.queens = queens

    def find_position(self, row):
        start = self.queens[row] + 1
        for column in range(start, SearchPositionImpl.SIZE):
            if self.is_valid(row, column):
                return column
        return -1

    def is_valid(self, row, column):
        for i in range(1, row + 1):
            if (self.queens[row - i] == column or
                self.queens[row - i] == column - i or
                self.queens[row - i] == column + i):
                return False
        return True
