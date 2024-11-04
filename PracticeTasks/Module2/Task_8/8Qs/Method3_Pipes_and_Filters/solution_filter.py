import multiprocessing
from board import Board

def solution_filter(input_pipe: multiprocessing.Pipe, output_pipe: multiprocessing.Pipe):
    try:
        while True:
            board = input_pipe.recv()
            output_pipe.send(board.solution())
    except EOFError:
        # Close the output pipe when there are no more solutions to process
        output_pipe.close()
