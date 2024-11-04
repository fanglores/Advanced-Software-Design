import multiprocessing
from board import Board

def placement_filter(input_pipe: multiprocessing.Pipe, output_pipe: multiprocessing.Pipe):
    try:
        while True:
            board = input_pipe.recv()
            place_queens(board, 0, output_pipe)
    except EOFError:
        # Close the output pipe when there are no more boards to process
        output_pipe.close()

def place_queens(board: Board, row: int, output_pipe: multiprocessing.Pipe):
    if row == board.size:
        output_pipe.send(board)
    else:
        for col in range(board.size):
            if board.is_safe(row, col):
                board.place_queen(row, col)
                place_queens(board, row + 1, output_pipe)
                board.remove_queen(row)
