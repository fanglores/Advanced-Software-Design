from typing import List

class Board:
    def __init__(self, size: int):
        self.size = size
        self.queens = [-1] * size

    def place_queen(self, row: int, col: int):
        self.queens[row] = col

    def remove_queen(self, row: int):
        self.queens[row] = -1

    def is_safe(self, row: int, col: int) -> bool:
        for r in range(row):
            c = self.queens[r]
            if c == col or abs(c - col) == abs(row - r):
                return False
        return True

    def solution(self) -> List[int]:
        return self.queens[:]
