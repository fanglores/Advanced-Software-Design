from find_queen_position_impl import FindQueenPositionImpl

class SearchPositionImpl:
    SIZE = 8

    def __init__(self):
        self.queens = [-1] * self.SIZE
        self.find_queen_position = FindQueenPositionImpl(self.queens)

    def search(self):
        row = 0
        while row >= 0 and row < self.SIZE:
            column = self.find_queen_position.find_position(row)
            if column < 0:
                self.queens[row] = -1
                row -= 1
            else:
                self.queens[row] = column
                row += 1
        return self.queens
