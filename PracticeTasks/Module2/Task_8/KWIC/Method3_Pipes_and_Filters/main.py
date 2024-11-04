from pipe import Pipe
from input_filter import InputFilter
from circular_shift_filter import CircularShiftFilter
from alphabetizer_filter import AlphabetizerFilter
from output_filter import OutputFilter

def run_kwic_pipeline(input_lines):
    # Create pipes to connect filters
    pipe_input_to_shift = Pipe()
    pipe_shift_to_alphabetize = Pipe()
    pipe_alphabetize_to_output = Pipe()

    # Instantiate filter threads
    input_filter = InputFilter(pipe_input_to_shift, input_lines)
    circular_shift_filter = CircularShiftFilter(pipe_input_to_shift, pipe_shift_to_alphabetize)
    alphabetizer_filter = AlphabetizerFilter(pipe_shift_to_alphabetize, pipe_alphabetize_to_output)
    output_filter = OutputFilter(pipe_alphabetize_to_output)

    # Start filter threads
    input_filter.start()
    circular_shift_filter.start()
    alphabetizer_filter.start()
    output_filter.start()

    # Wait for all threads to complete
    input_filter.join()
    circular_shift_filter.join()
    alphabetizer_filter.join()
    output_filter.join()

if __name__ == "__main__":
    print("Enter lines of text for the KWIC system (press Enter on an empty line to finish):")
    input_lines = []
    while True:
        line = input(">> ")
        if line == "":
            break
        input_lines.append(line)

    run_kwic_pipeline(input_lines)
