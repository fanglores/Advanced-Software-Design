from event_manager import *

def is_position_safe(position):
    x1, y1 = position
    for x2, y2 in queens:
        if x2 == x1 or y2 == y1 or x2 - y2 == x1 - y1 or x2 + y2 == x1 + y1:
            return False
    return True

def place_initial_queen(position):
    queens.append(position)
    evManager.fire(IEvents.QUEEN_PLACED_EVENT, 1)

def place_queen(row):
    if row == 8:
        evManager.fire(IEvents.FINISHED_EVENT)
    else:
        for col in range(8):
            if is_position_safe((row, col)):
                queens.append((row, col))
                evManager.fire(IEvents.QUEEN_PLACED_EVENT, row + 1)
                queens.pop()

def display_solution():
    print("Solution:")
    board = [["-" for _ in range(8)] for _ in range(8)]
    for row, col in queens:
        board[row][col] = "Q"
    for row in board:
        print(" ".join(row))
    print()

evManager = EventManager()

queens = []
evManager.subscribe(IEvents.INITIAL_SET_EVENT, place_initial_queen)
evManager.subscribe(IEvents.QUEEN_PLACED_EVENT, place_queen)
evManager.subscribe(IEvents.FINISHED_EVENT, display_solution)

x_input, y_input = [int(x) for x in input('Initial position (x y): ').split()]
evManager.fire(IEvents.INITIAL_SET_EVENT, (x_input, y_input))
