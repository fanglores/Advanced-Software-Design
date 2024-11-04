import multiprocessing
from input_filter import input_filter
from placement_filter import placement_filter
from solution_filter import solution_filter
from output_filter import output_filter

def main():
    size = 8  # Size of the chessboard for the Eight Queens problem

    # Set up pipes for communication between filters
    input_pipe_parent, input_pipe_child = multiprocessing.Pipe()
    placement_pipe_parent, placement_pipe_child = multiprocessing.Pipe()
    solution_pipe_parent, solution_pipe_child = multiprocessing.Pipe()

    # Initialize and start processes for each filter
    input_process = multiprocessing.Process(target=input_filter, args=(input_pipe_child, size))
    placement_process = multiprocessing.Process(target=placement_filter, args=(input_pipe_parent, placement_pipe_child))
    solution_process = multiprocessing.Process(target=solution_filter, args=(placement_pipe_parent, solution_pipe_child))
    output_process = multiprocessing.Process(target=output_filter, args=(solution_pipe_parent,))

    # Start all processes
    input_process.start()
    placement_process.start()
    solution_process.start()
    output_process.start()

    # Close the writing end of each pipe in the main process after starting the filters
    input_pipe_child.close()
    placement_pipe_child.close()
    solution_pipe_child.close()

    # Wait for all processes to complete
    input_process.join()
    placement_process.join()
    solution_process.join()
    output_process.join()

if __name__ == "__main__":
    main()
