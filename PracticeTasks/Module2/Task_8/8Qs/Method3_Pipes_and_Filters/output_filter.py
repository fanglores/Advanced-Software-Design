import multiprocessing

def output_filter(input_pipe: multiprocessing.Pipe):
    try:
        while True:
            solution = input_pipe.recv()
            print("Solution:", solution)
    except EOFError:
        pass  # Exit when no more data is available
