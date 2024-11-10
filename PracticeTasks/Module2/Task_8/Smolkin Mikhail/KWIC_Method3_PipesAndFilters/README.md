# Key Word in Context - PipesAndFilters

## Task Description

This program solves the **KWIC** problem, where index system accepts an ordered set of lines, each line is an ordered set of words, and each word is an ordered set of characters. Any line may be *circularly shifted* by repeatedly removing the first word and appending it at the end of the line. The KWIC index system outputs a listing of all circular shifts of all lines in alphabetical order.

## Project Structure

The project is organized in a modular structure:
```
KWIC_Method3_PipesAndFilters/
├── alphabetizer_filter.py   # Filter with a alphabetizer (sorter)
├── circular_shift_filter.py # Filter performing circularly shift
├── input_filter.py          # Filter for input
├── main.py                  # Main file for running the pipeline
├── output_filter.py         # Filter for output
├── pipe.py                  # Pipe implementation
└── README.md                # Documentation file with project description and usage instructions
```

### Requirements

- Python 3.6 or higher

## Running the Program

1. Clone or download the project repository.
2. Run the program with the following command:
```bash
python main.py
```
### Input and Output Example

**Sample Input** (entered during program execution):
```
Enter lines of text for the KWIC system (press Enter on an empty line to finish):
>> first second third
>> fourth fifth                       
>> 
fifth fourth
first second third
fourth fifth
second third first
third first second
```

**Sample Output**:
```
fifth fourth
first second third
fourth fifth
second third first
third first second
```
## Explanation

1. **PipesAndFilters Approach**: The program build like a pipeline with independent filters
2. **Pipeline**:
    - The program waits for input from user;
    - The program starts by creating instances of pipes and running threads with filters;
    - The program waits for all threads to complete.

### Additional Notes

- The program outputs a listing of all circular shifts of all lines in alphabetical order.
- The pipes and filters approach makes it easy to modify or extend functionality by adding new filters or modifing presented.