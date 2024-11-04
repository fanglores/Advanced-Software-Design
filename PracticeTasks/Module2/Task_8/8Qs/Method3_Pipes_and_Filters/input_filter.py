import multiprocessing
from board import Board

def input_filter(output_pipe: multiprocessing.Pipe, size: int):
    board = Board(size)
    output_pipe.send(board)
    output_pipe.close()  # Close the output pipe after sending data
